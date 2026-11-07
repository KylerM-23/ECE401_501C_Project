import json
import tkinter as tk
import WrappedGuiFunctions as GUI
import random
import sqlite3
from DBFunctions import *

def display_wrapped(cursor, user_id):
    json_string = ""

    query = f"""
            SELECT json_wrap
            FROM user_wrap
            WHERE ID = {user_id}
            """
    json_strings = exeute_query(cursor, query, print_query = False) #get the json string from the user_wrap table
    json_string = json_strings[0]

    top_artists = [None, None, None]
    top_songs = [None, None, None]

    wrapped_attributes = json.loads(json_string) # Convert the JSON string into a Python list of dictionaries

    for wrap in wrapped_attributes:
        if (wrap['type'] == 'Artist Rank'):
            for rank, artist in enumerate(wrap["artist"]):
                top_artists[rank] = artist
    
        if (wrap['type'] == 'Song Rank'):
            for rank, track in enumerate(wrap["track"]):
                top_songs[rank] = (track["track"], track["artist"])        
        

    root = tk.Tk()

    # Configure the window settings
    root.title("Your Music Wrapped")
    root.geometry("800x800")  # Width x Height in pixels

    GUI.rainbow_bg(root, random.randint(1, 5000))
    GUI.final_summary(root, top_songs, top_artists)

    root.mainloop()

if __name__ == "__main__":
    db = sqlite3.connect("music.db")
    cursor = db.cursor() #Create a cursor object to execute SQL commands
    
    query = """
            SELECT ID
            FROM user_wrap
            """
    
    users = exeute_query(cursor, query, print_query = False)
    
    user_id = random.choice(users)
    
    display_wrapped(cursor, user_id[0])