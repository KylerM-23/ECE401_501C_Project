import json
import tkinter as tk
import WrappedGuiFunctions as GUI
import random

json_string = """
[
    {
        "type": "Artist Rank",
        "artist": ["AC/DC", "Black Sabbath", "Metallica"],
        "importance": 1
    },
    
    {
        "type": "Song Rank",
        "track":
        [
            {"artist": "AC/DC", "track": "Back In Black"},
            {"artist": "Black Sabbath", "track": "War Pigs"},
            {"artist": "Metallica", "track": "Master of Puppets"}
        ],
        "importance": 1
    },
    
    {
        "type": "Ear Worm",
        "track_id": 12345,
        "listens": 1000,
        "importance": 1
    }
]
"""

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
