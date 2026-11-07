import json
import sqlite3

# Subquery that turns a track's artists into one string ("Artist A, Artist B")
ARTISTS_OF_TRACK = """(SELECT GROUP_CONCAT(artist, ', ')
                       FROM track_artist ta
                       WHERE ta.track_id = t.track_id)"""


def get_top_artists(cursor, user_id, limit=3):
    cursor.execute("""
        SELECT artist, SUM(listen_count) AS plays
        FROM listen JOIN track_artist USING (track_id)
        WHERE user_id = ?
        GROUP BY artist
        ORDER BY plays DESC, artist
        LIMIT ?;
        """, (user_id, limit))

    return [row[0] for row in cursor.fetchall()]


def get_top_songs(cursor, user_id, limit=3):
    cursor.execute(f"""
        SELECT t.track_id, t.track_name, {ARTISTS_OF_TRACK}, l.listen_count
        FROM listen l JOIN tracks t ON l.track_id = t.track_id
        WHERE l.user_id = ?
        ORDER BY l.listen_count DESC, t.track_name
        LIMIT ?;
        """, (user_id, limit))

    return cursor.fetchall()   # (track_id, track_name, artists, listen_count)


def get_total_songs(cursor, user_id):
    cursor.execute("SELECT COUNT(*) FROM listen WHERE user_id = ?;", (user_id,))
    return cursor.fetchone()[0]

# Total Minutes Per User
def get_total_minutes(cursor, user_id):
    cursor.execute("""
        SELECT SUM(t.duration_ms) / 60000.0
        FROM listen l JOIN tracks t ON l.track_id = t.track_id
        WHERE l.user_id = ?;
        """, (user_id,))

    total_minutes = cursor.fetchone()[0]
    return total_minutes if total_minutes is not None else 0

# Total Minutes Across All Users
def get_global_minutes(cursor):
    cursor.execute("""
        SELECT SUM(t.duration_ms) / 60000.0
        FROM listen l JOIN tracks t ON l.track_id = t.track_id;
        """)
    global_minutes = cursor.fetchone()[0]
    return global_minutes if global_minutes is not None else 0

def get_hidden_gem(cursor, user_id):
    # Hidden gem = a track the user loves that few other people know:
    # favorites first, then lowest popularity.
    cursor.execute(f"""
        SELECT t.track_id, t.track_name, {ARTISTS_OF_TRACK}, t.popularity
        FROM listen l JOIN tracks t ON l.track_id = t.track_id
        WHERE l.user_id = ? AND t.popularity IS NOT NULL
        ORDER BY l.favorite DESC, t.popularity ASC, l.listen_count DESC
        LIMIT 1;
        """, (user_id,))

    return cursor.fetchone()   # None if the user has no listens


def build_wrapped_json(cursor, user_id):
    """Returns the Wrapped data for one user as a JSON string."""
    wrapped = []

    top_artists = get_top_artists(cursor, user_id)
    if top_artists:
        wrapped.append({
            "type": "Artist Rank",
            "artist": top_artists,
            "importance": 1
        })

    top_songs = get_top_songs(cursor, user_id)
    if top_songs:
        wrapped.append({
            "type": "Song Rank",
            "track": [{"artist": s[2], "track": s[1]} for s in top_songs],
            "importance": 1
        })

        # Ear Worm = the single most-listened track (first row of top songs)
        ear = top_songs[0]
        wrapped.append({
            "type": "Ear Worm",
            "track_id": ear[0],
            "track": ear[1],
            "artist": ear[2],
            "listens": ear[3],
            "importance": 1
        })

    total = get_total_songs(cursor, user_id)
    wrapped.append({
        "type": "Total Songs",
        "total": total,
        "importance": 1
    })

    gem = get_hidden_gem(cursor, user_id)
    if gem:
        wrapped.append({
            "type": "Hidden Gem",
            "track_id": gem[0],
            "track": gem[1],
            "artist": gem[2],
            "popularity": gem[3],
            "importance": 1
        })

    return json.dumps(wrapped, indent=2)


if __name__ == "__main__":
    db = sqlite3.connect("music.db")
    cursor = db.cursor()

    try:
        print(build_wrapped_json(cursor, 23))
    finally:
        db.close()
