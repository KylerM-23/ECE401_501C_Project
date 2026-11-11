import sqlite3, os, time
import pandas as pd

import CreateDataBase as CDB
import AddData as Data
import WrappedQueries as WQ

if __name__ == "__main__":
    delete = 0
    
    try:
        if os.path.isfile("music.db"):
            os.remove("music.db")
            
        db = sqlite3.connect("music.db") #Open/create database file
        cursor = db.cursor()   #Create a cursor object to execute SQL commands

        CDB.load_data(db, "songs", "Data/songs.csv")        
        db.commit()	#save changes to DB
        
        #SQLITE does not allow for tables to add new constraints for primary keys
        #Need to recreate the tables and add constraints. :(
        
        CDB.create_tables(cursor)
        CDB.separate_track_artists(cursor)
        CDB.fill_track_tables(cursor)
        CDB.create_index(cursor)
        
        cursor.execute("DROP TABLE songs;") #we are done using songs and can delete it
        db.commit()	#save changes to DB
        db.close()
        
        db = sqlite3.connect("music.db") #Open/create database file
        cursor = db.cursor()   #Create a cursor object to execute SQL commands
        
        Data.create_artist_accounts(cursor)
        Data.add_random_users(cursor, 200)

        Data.addUser(cursor, "Kyler", uID = 23)
        Data.addListen(cursor, Data.find_track_ID(cursor, artist_name = 'Sabaton', track_name = "The Attack of the Dead Men"), 23, 1, 1)
        Data.addListen(cursor, Data.find_track_ID(cursor, album_name = 'Random Access Memories', track_name = "Instant Crush (feat. Julian Casablancas)"), 23, 1, 1)
        Data.addListen(cursor, Data.find_track_ID(cursor, track_name = "Forgot About Dre"), 23, 1, 1)
        Data.addListen(cursor, Data.find_track_ID(cursor, artist_name = 'Linkin Park', track_name = "Papercut"), 23, 1, 1)
        Data.addListen(cursor, Data.find_track_ID(cursor, album_name = 'Arrival', track_name = "Dancing Queen"), 23, 1, 0)
        Data.addListen(cursor, Data.find_track_ID(cursor, artist_name = 'Korn', track_name = "Freak On a Leash"), 23, 1, 1)

        db.commit()
        db.close()
        
        db = sqlite3.connect("music.db") #Open/create database file
        cursor = db.cursor()   #Create a cursor object to execute SQL commands
        
        WQ.create_wrapped_json_users(cursor)
        db.commit()
        
        db.close()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        delete = 1

    finally:
        db.close()

        if delete == 1:
            os.remove("music.db")
