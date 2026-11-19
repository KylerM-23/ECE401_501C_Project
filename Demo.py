import sqlite3, os, time
import pandas as pd

def load_data_small(db, file):
    df = pd.read_csv(file, usecols=['track_id', 'artists', 'track_name']) #only save 3 cols
    df.to_sql("songs", db, if_exists="replace", index=False) 

def load_data(db, file):
    df = pd.read_csv(file)
    df.to_sql("songs", db, if_exists="replace", index=False) 

def execute_query(cursor, query, display_query = True, display_results = True, return_time = False):
    cursor.execute(query)
    
    t = time.perf_counter_ns()
    
    if display_query:
        print(query)
        
    if display_results:
        for row in cursor.fetchall():
            print(row)
        
    if return_time:
        return t

def display_db(cursor):
    query = """
        SELECT *
        FROM songs
        """
    
    execute_query(cursor, query, display = False)

try:
    db = [sqlite3.connect("demo1.db"), sqlite3.connect("demo2.db")]		#Open/create database file
    
    cursor = [db[0].cursor(), db[1].cursor()] 					#Create a cursor object to execute SQL commands
    
    query = """
            SELECT track_id
            FROM songs
            WHERE track_name = "Highway To Hell" AND album_name = "Highway To Hell"
            """
    sum_ = 0
    for i in range(100):
        load_data(db[0], "Data/dataset.csv")

        start_time = time.perf_counter_ns()

        end_time = execute_query(cursor[0], query, display_results = False, display_query = (i == 0), return_time = True)

        sum_ += (end_time - start_time) / 1000 /1000
            
    print("Full Dataset\t", (sum_) / 100, 'ms')
    db[0].commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    for i in range(2):
        db[i].close()
