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
        
        