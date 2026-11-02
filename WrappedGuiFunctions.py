import tkinter as tk

POS_MAX = 6000
division = POS_MAX/6
slope = 255/division


def rainbow_bg(root, POS):
    POS += 0.5
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
    
    R = str(hex(int(R)))[2:]
    G = str(hex(int(G)))[2:]
    B = str(hex(int(B)))[2:]
    
    if (len(R) == 1):
        R = "0" + R
    if (len(G) == 1):
        G = "0" + G
    if (len(B) == 1):
        B = "0" + B
    
    color = "#"+ R + G + B
    
    root.configure(bg = color)  
    root.after(1, rainbow_bg, root, POS)
    
def final_summary(root, top_songs, top_artists):
    welcome_lb = tk.Label(root, text="Welcome To Music Wrapped: 2026")
    welcome_lb.pack(pady=20)
    
    top_track_lb = tk.Label(root, text="Top Songs:")
    top_track_lb.pack(pady=20)
    
    top_tracks_lb = [None, None, None]
    
    for rank, track in enumerate(top_songs):
        if (track != None):
            top_tracks_lb[rank] = tk.Label(root, text = f"{rank+1}. {track[0]} by {track[1]}")
            top_tracks_lb[rank].pack(pady=20)
        
    top_artist_lb = tk.Label(root, text="Top Artists:")
    top_artist_lb.pack(pady=20)
    
    top_artists_lb = [None, None, None]
    
    for rank, artist in enumerate(top_artists):
        if (artist != None):
            top_artists_lb[rank] = tk.Label(root, text = f"{rank+1}. {artist}")
            top_artists_lb[rank].pack(pady=20)

