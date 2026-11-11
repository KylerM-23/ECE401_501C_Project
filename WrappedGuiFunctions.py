import tkinter as tk
import random
import textwrap

POS_MAX = 6000
division = POS_MAX/6
slope = 255/division

FONT = ("Arial", 15)
BIG_FONT = ("Arial", 16)
TOTAL_FONT = ("Arial", 17, "bold")

PADDING = 5
PADX = PADDING
PADY = PADDING*3
MAX_CHAR = 50

index = 0

def rainbow_bg(root, POS):
    POS += 10
    if (POS > POS_MAX):
        POS = 0
    
    if (POS < division):
        R = 255
        G = slope * (POS)
        B = 0
    elif (POS < 2*division):
        R = -slope * (POS - division) + 255
        G = 255
        B = 0
    elif (POS < 3*division):
        R = 0
        G = 255
        B = slope * (POS - 2 * division) 
    elif (POS < 4*division):
        R = 0
        G = -slope * (POS - 3 * division) + 255
        B = 255
    elif (POS < 5*division):
        R = slope * (POS - 4 * division)
        G = 0
        B = 255
    elif (POS < 6*division):
        R = 255
        G = 0
        B = -slope * (POS - 5 * division) + 255
    else:
        R = 255
        G = 0
        B = 0
    
    color = f"#{int(R):02x}{int(G):02x}{int(B):02x}"
    root.configure(bg = color)
    root.after(16, rainbow_bg, root,POS)
    
def process_string(string):
    new_string = textwrap.fill(string, width = MAX_CHAR)
    return new_string

def process_wrap(wrapped_dictionary, wrapped_attributes):
    for wrap in wrapped_attributes:
        if (wrap['type'] == 'Artist Rank'):
            for rank, artist in enumerate(wrap["artist"]):
                wrapped_dictionary["top_artists"][rank] = artist

        elif (wrap['type'] == 'Song Rank'):
            for rank, track in enumerate(wrap["track"]):
                wrapped_dictionary["top_songs"][rank] = (track["track"], track["artist"])
        
        elif (wrap['type'] == 'Minutes'):
            wrapped_dictionary["minutes"] = wrap["mins"]
        
        elif (wrap['type'] == 'Rank'):
            wrapped_dictionary["rank"] = wrap["rank"]
        
        elif (wrap['type'] == 'Hidden Gem'):
            string = f"Your Hidden Gem was \"{wrap['track']}\" by {wrap['artist']} with a popularity score of {wrap['popularity']}/100. Good job digging that one up!"
            wrapped_dictionary["other"].append(string)
        
        elif (wrap['type'] == 'Ear Worm'):
            string = f"You couldn't get enough of \"{wrap['track']}\" by {wrap['artist']}. You caught an ear worm, listening to it {wrap['listens']} times."
            wrapped_dictionary["other"].append(string)
            
def update_wrapped(root, label, wrapped_dictionary):
    global index
    
    max_char = 100
    
    if (index == len(wrapped_dictionary["other"])):
        index = 0
    data = wrapped_dictionary["other"][index]
    
    string = textwrap.fill(data, width = max_char)
    
    label.config(text = string)
    
    index+=1
    
    #create updating loop to change which of the small wraps is being displayed
    root.after(30000, update_wrapped, root, label, wrapped_dictionary)
    
def final_summary(root, wrapped_attributes, num_users):
    wrapped_dictionary = {
        "top_artists": [None, None, None],
        "top_songs" : [None, None, None],
        "minutes": 0,
        "rank": 0,
        "other": []
        }
    
    process_wrap(wrapped_dictionary, wrapped_attributes)
    
    main_frame = tk.Frame(root, width = 1200, height = 1000)
    main_frame.grid(row = 0, column = 0, padx=30, pady=30, sticky="nsew")

    main_frame.columnconfigure(0, weight=1, uniform="side_by_side")
    main_frame.columnconfigure(1, weight=1, uniform="side_by_side")

    welcome_lb = tk.Label(main_frame, text="Welcome To Music Wrapped: 2026", font = TOTAL_FONT)
    welcome_lb.grid(row = 0, column = 0, columnspan = 2, padx=PADX, pady=PADY)
    
    #TOP TRACKS
    track_frame = tk.Frame(main_frame)
    track_frame.grid(row = 1, column = 0, padx=PADX, pady=PADY)
    
    top_track_lb = tk.Label(track_frame, text="Top Songs:", font = FONT)
    top_track_lb.grid(row = 0, column = 0, padx=PADX, pady=PADY)
    
    top_tracks_lb = [None, None, None]
    
    for rank, track in enumerate(wrapped_dictionary["top_songs"]):
        if (track != None):
            string = process_string(f"{rank+1}. {track[0]} by {track[1]}")
            top_tracks_lb[rank] = tk.Label(track_frame, text = string, font = FONT, width = 50, anchor = "w", justify = "left")
            top_tracks_lb[rank].grid(row = 1 + rank, column = 0, padx=PADX, pady=PADY)
    
    #TOP ARTISTS        
    artist_frame = tk.Frame(main_frame)
    artist_frame.grid(row = 1, column = 1, padx=PADDING, pady=PADDING)
    
    top_artist_lb = tk.Label(artist_frame, text="Top Artists:", font = FONT)
    top_artist_lb.grid(row = 0, column = 0, padx=PADX, pady=PADY)
    
    top_artists_lb = [None, None, None]
    
    for rank, artist in enumerate(wrapped_dictionary["top_artists"]):
        if (artist != None):
            string = process_string(f"{rank+1}. {artist}")
            top_artists_lb[rank] = tk.Label(artist_frame, text = string, font = FONT, width = 35, anchor = "w")
            top_artists_lb[rank].grid(row = 1 + rank, column = 0, padx=PADX, pady=PADY)
    
    #NUM MINUTES
    num_minutes = wrapped_dictionary["minutes"]
    minutes_lb = tk.Label(main_frame, text=f"Minutes Listened: {num_minutes}", font = FONT)
    minutes_lb.grid(row = 3, column = 0, padx=PADX, pady=PADY*2)
    
    #NUM RANK
    rank_minutes = wrapped_dictionary["rank"]
    total_min_lb = tk.Label(main_frame, text=f"Global Rank: {rank_minutes}%", font = FONT)
    total_min_lb.grid(row = 3, column = 1, padx=PADX, pady=PADY*2)
    
    wrapped_label = tk.Label(main_frame, text="", font = BIG_FONT)
    wrapped_label.grid(row = 5, column = 0, columnspan = 2, padx=PADX, pady=PADY)
            
    global index
    index = random.randint(0, len(wrapped_dictionary["other"])-1)
    
    update_wrapped(root, wrapped_label, wrapped_dictionary)

