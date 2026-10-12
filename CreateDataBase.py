import sqlite3, os, time
import pandas as pd
from CreateTables import *
from GetArtists import *

delete = 0

# If the table exists, the program will fail and delete the one already found
# Just re-run. Will come up with a better solution later.

try:
    if os.path.isfile("music.db"):
        os.remove("music.db")
        
    db = sqlite3.connect("music.db") #Open/create database file

    cursor = db.cursor()   #Create a cursor object to execute SQL commands

    load_data(db, "songs", "Data/songs.csv")
    
    db.commit()	#save changes to DB
    
    #SQLITE does not allow for tables to add new constraints for primary keys
    #Need to recreate the tables and add constraints. :(
    
    create_tables(cursor)
    
    seperate_track_artists(cursor)
    
    cursor.execute(
        '''
        INSERT INTO track_genre(track_id, track_genre)   
        
        SELECT DISTINCT track_id, track_genre
        FROM songs
        GROUP BY track_id;
        ''')
    
    cursor.execute(
        '''
        INSERT INTO tracks (track_id, album_name, track_name, popularity,
            duration_ms, explicit)
            
        SELECT DISTINCT track_id, album_name, track_name, popularity,
            duration_ms, explicit
        FROM songs
        WHERE album_name IS NOT NULL
        GROUP BY track_id;
        ''')       
    
    cursor.execute(
        '''
        INSERT INTO track_attributes (track_id, danceability, energy, key, loudness, mode,
            speechiness, acousticness, instrumentalness, liveness, valence, tempo,
            time_signature)
        
        SELECT DISTINCT track_id, danceability, energy, key, loudness, mode, speechiness, acousticness,
            instrumentalness, liveness, valence, tempo, time_signature
        FROM songs
        GROUP BY track_id;
        ''')
    
    
    
    db.commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    delete = 1

finally:
    db.close()

    if delete == 1:
        os.remove("music.db")