import sqlite3, os, time
import pandas as pd

delete = 0

# If the table exists, the program will fail and delete the one already found
# Just re-run. Will come up with a better solution later.

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
            track_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            listen_count INTEGER,
            favorite INTEGER,
            
            PRIMARY KEY (track_id, user_id),
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
            FOREIGN KEY (user_id) REFERENCES users(ID)
            );
        ''')
    
def seperate_track_artists(cursor):
    cursor.execute('''
        SELECT DISTINCT track_id, artists
        FROM songs
        WHERE track_id IS NOT NULL AND artists IS NOT NULL
    ''')
    
    songs = cursor.fetchall()
    
    normalized_data = []
    
    for song in songs:
        if ';' in song[1]:
            split_song = song[1].split(';')
            for artist in split_song:
                normalized_data.append((song[0], artist))
        else:
            normalized_data.append((song[0], song[1]))
            
    for song in normalized_data:
        query = "INSERT INTO track_artist (track_id, artist) VALUES (?, ?);"
        
        try:
            cursor.execute(query, (song[0], song[1]))
        except:
            print(query)
        
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
    
    cursor.execute("DROP TABLE songs;") #we are done using songs and can delete it
    
    db.commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    delete = 1

finally:
    db.close()

    if delete == 1:
        os.remove("music.db")