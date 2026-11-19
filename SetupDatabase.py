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
        Data.add_random_users(cursor, 100)
        Data.load_team_data(cursor, "Data/User_Wrapped.csv")

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

        if delete == 1:
            os.remove("music.db")
