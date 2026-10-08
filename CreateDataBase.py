import sqlite3, os, time
import pandas as pd

delete = 0

# If the table exists, the program will fail and delete the one already found
# Just re-run. Will come up with a better solution later.

def load_data(db, table_name, file):
    df = pd.read_csv(file)
    df.to_sql(table_name, db, if_exists="replace", index=False) 

try:
    db = sqlite3.connect("music.db") #Open/create database file

    cursor = db.cursor()   #Create a cursor object to execute SQL commands

    load_data(db, "tracks", "Data/tracks.csv")
    load_data(db, "track_attributes", "Data/track_attributes.csv")
    
    cursor.execute(
        '''
        CREATE TABLE users (
            ID INTEGER PRIMARY KEY NOT NULL,
            name VARCHARACTER(20)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE artist (
            ID INTEGER PRIMARY KEY NOT NULL,
            num_listeners INTEGER,
            num_tracks INTEGER,
            num_albums INTEGER,
            time_listened INTEGER,
            
            FOREIGN KEY (ID) REFERENCES users(ID)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE listener (
            ID INTEGER PRIMARY KEY NOT NULL,
            age INTEGER NOT NULL,
            
            FOREIGN KEY (ID) REFERENCES users(ID)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE admin (
            ID INTEGER PRIMARY KEY NOT NULL,
            rank VARCHARACTER(20),
            
            FOREIGN KEY (ID) REFERENCES users(ID)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE listen (
            TRACKID INTEGER NOT NULL,
            USERID INTEGER NOT NULL,
            listen_count INTEGER,
            favorite INTEGER,
            
            PRIMARY KEY (TRACKID, USERID),
            FOREIGN KEY (TRACKID) REFERENCES tracks(track_id)
            FOREIGN KEY (USERID) REFERENCES users(ID)
            );
        ''')
    
    db.commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    delete = 1

finally:
    db.close()

    if delete == 1:
        os.remove("music.db")