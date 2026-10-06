import sqlite3, os, time
import pandas as pd

def load_data(db, table_name, file):
    df = pd.read_csv(file)
    df.to_sql(table_name, db, if_exists="replace", index=False) 

try:
    db = sqlite3.connect("music.db") #Open/create database file

    cursor = db.cursor()   #Create a cursor object to execute SQL commands

    load_data(db, "tracks", "Data/tracks.csv")
    load_data(db, "track_attributes", "Data/track_attributes.csv")
    
    #create the Listen relation
    #create the user and so on relations

    db.commit()	#save changes to DB

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    db.close()
