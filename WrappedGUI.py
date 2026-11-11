import json
import tkinter as tk
import WrappedGuiFunctions as GUI
import random
import sqlite3
from DBFunctions import *

def display_wrapped(cursor, user_id, user_len):
    json_string = ""

    query = f"""
            SELECT json_wrap
            FROM user_wrap
            WHERE ID = {user_id}
            """
    json_strings = exeute_query(cursor, query, print_query = False) #get the json string from the user_wrap table
    json_string = json_strings[0][0]

    wrapped_attributes = json.loads(json_string) # Convert the JSON string into a Python list of dictionaries

    root = tk.Tk()

    # Configure the window settings
    root.title("Your Music Wrapped")
    root.geometry("1200x800")  # Width x Height in pixels
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    main_frame = tk.Frame(root, width = 1200, height = 1000)
    main_frame.grid(row = 0, column = 0, padx=5, pady=5, sticky="nsew")

    main_frame.columnconfigure(0, weight=1, uniform="side_by_side")
    main_frame.columnconfigure(1, weight=1, uniform="side_by_side")

    GUI.rainbow_bg(root, main_frame, random.randint(1, 5000))
    GUI.final_summary(root, main_frame, wrapped_attributes, user_len)

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
    
    display_wrapped(cursor, user_id[0], len(user_id))