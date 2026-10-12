import sqlite3, os, time
import pandas as pd

def load_data(db, table_name, file):
    df = pd.read_csv(file)
    df.to_sql(table_name, db, if_exists="replace", index=False)

def create_tables(cursor):
    cursor.execute(
        '''
        CREATE TABLE tracks (
            track_id    TEXT PRIMARY KEY NOT NULL,
            album_name  TEXT NOT NULL,
            track_name  TEXT NOT NULL,
            popularity  INTEGER NOT NULL,
            duration_ms INTEGER NOT NULL,
            explicit    TEXT NOT NULL
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE track_genre (
            track_id    TEXT NOT NULL,
            track_genre TEXT NOT NULL,
            
            PRIMARY KEY (track_id, track_genre),
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE track_artist (
            track_id    TEXT NOT NULL,
            artist 		TEXT NOT NULL,
            
            PRIMARY KEY (track_id, artist),
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
            );
        ''')
    
    cursor.execute(
        '''
        CREATE TABLE track_attributes(
            track_id         TEXT PRIMARY KEY NOT NULL,
            danceability     REAL,
            energy           REAL,
            key              INTEGER,
            loudness         REAL,
            mode             INTEGER,
            speechiness      REAL,
            acousticness     REAL,
            instrumentalness REAL,
            liveness         REAL,
            valence          REAL,
            tempo            REAL,
            time_signature   INTEGER
            );
        ''')
    
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