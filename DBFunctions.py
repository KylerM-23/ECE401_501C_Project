import sqlite3

def exeute_query(cursor, query, print_query = False):
    if print_query:
        print(query)
    
    try:
        cursor.execute(query)
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    return

def find_track_ID(cursor, track_name, album_name = None, artist_name = None):
    
    predicate = f" WHERE track_name = '{track_name}'"
    
    if album_name is not None:
        predicate = predicate + f" AND album_name = '{album_name}'"
        
    if artist_name is not None:
        query = f"""
            WITH artist_temp(track_id) AS (
                SELECT DISTINCT track_id
                FROM track_artist
                WHERE artist = """ + "'" + artist_name + "')" + f"""
            
            SELECT DISTINCT track_id
            FROM tracks JOIN artist_temp USING (track_id)""" + predicate + ";"

    else:
        query = f"""
            SELECT DISTINCT track_id
            FROM tracks """ + predicate + ";"
        
    exeute_query(cursor, query)
    tracks = cursor.fetchall()
    
    if (len(tracks) > 0):
        if (len(tracks) > 1):
            print("Multiple Tracks returned. Returning the first result.")
            print(query)
            
        return tracks[0][0]
    else:
        print("No tracks found")
        print(query)
        return None
        
    