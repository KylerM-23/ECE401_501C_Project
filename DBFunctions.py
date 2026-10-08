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
        predicate = predicate + f" AND artists = '{artist_name}'"

    query = f"""
        SELECT DISTINCT track_id
        FROM tracks""" + predicate + ";"
        
    exeute_query(cursor, query)
    tracks = cursor.fetchall()
    
    if (len(tracks) > 0):
        if (len(tracks) > 1):
            print("Multiple Tracks returned. Returning the first result.")
        return tracks[0][0]
    else:
        return None
        
    