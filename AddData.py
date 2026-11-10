import sqlite3
from DBFunctions import *
import random

def generate_userID(uID):
    if uID != None:	#Programmer has overriden the ID generation
        return uID
    
    done = False
    
    counter = 0
    
    while(True):
        uID_temp = random.randint(100000, 999999)
        uID_check = exeute_query(cursor, f"""SELECT ID FROM users WHERE ID = {uID_temp};""")
        
        if len(uID_check) == 0:
            return uID_temp
        elif counter == 1000:	#way to escape the loop
            return -1
        counter+=1
    

def addUser(cursor, uName, uID = None):
    ID = generate_userID(uID)
    if(ID == -1):
        return
        
    query = f"""
        INSERT INTO users (ID, name)
            VALUES 	(?, ?);
        """
    
    cursor.execute(query, (ID, uName))
    
    return ID

def addArtist(cursor, aName):
    return addUser(cursor, aName)

def addListen(cursor, tID, uID, listensNum, fav):
    if tID is None:
        return
    
    query = f"""
            INSERT INTO listen (track_id, user_id, listen_count, favorite)
                VALUES 	('{tID}', {uID}, {listensNum}, {fav});
            """
    
    return exeute_query(cursor, query)

def create_artist_accounts(cursor):
    all_artists = get_artists(cursor)
    
    for artist in all_artists:
        addArtist(cursor, artist[0])
    

def add_random_users(cursor, num_users):
    users = []
    
    all_artists = get_artists(cursor)
    
    for user in range(0, num_users):
        random_artist_num = random.randint(1, 20)		#covers people who listen to a few artists to the super fan
        
        uID = addUser(cursor, f"BOT{user}")	#add n number of users
        
        ran_artists = random.sample(all_artists, random_artist_num)
        
        track_ids = []
        
        for artist in ran_artists:
            
            query = """
                SELECT DISTINCT track_id
                FROM track_artist
                WHERE artist = ?;"""
        
            cursor.execute(query, (artist[0],))
            tracks = cursor.fetchall()
            
            for t_id in tracks:
                if (int(random.uniform(0,1.99)) == 1):
                    fav = int(random.uniform(0,1.99))
                    addListen(cursor, t_id[0], uID, random.randint(1, 200), fav)
        


db = sqlite3.connect("music.db") #Open/create database file

cursor = db.cursor()   #Create a cursor object to execute SQL commands

create_artist_accounts(cursor)

add_random_users(cursor, 200)




addUser(cursor, "Kyler", uID = 23)
addListen(cursor, find_track_ID(cursor, artist_name = 'Sabaton', track_name = "The Attack of the Dead Men"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, album_name = 'Random Access Memories', track_name = "Instant Crush (feat. Julian Casablancas)"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, track_name = "Forgot About Dre"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, artist_name = 'Linkin Park', track_name = "Papercut"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, album_name = 'Arrival', track_name = "Dancing Queen"), 23, 1, 0)
addListen(cursor, find_track_ID(cursor, artist_name = 'Korn', track_name = "Freak On a Leash"), 23, 1, 1)


db.commit()
db.close()