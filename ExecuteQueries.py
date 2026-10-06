import sqlite3, os

def execute_query_timed(cursor, query, display_query = True, display_results = True, return_time = False):
    cursor.execute(query)
    
    t = time.perf_counter_ns()
    
    if display_query:
        print(query)
        
    if display_results:
        for row in cursor.fetchall():
            print(row)
        
    if return_time:
        return t
    
def execute_query(cursor, query, display_query = True, display_results = True):
    cursor.execute(query)
    
    if display_query:
        print(query)
        
    if display_results:
        for row in cursor.fetchall():
            print(row)

try:
    db = sqlite3.connect("music.db")
    cursor = db.cursor() #Create a cursor object to execute SQL commands
    
    query = """
            SELECT artists, track_name
            FROM tracks
            WHERE artists = "AC/DC"
            """
    
    execute_query(cursor, query, display_results = True, display_query = True)
    db.commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    db.close()


