import sqlite3
from DBFunctions import *

def addUser(cursor, uID, uName):
    query = f"""
        INSERT INTO users (ID, name)
            VALUES 	({uID}, '{uName}');
        """
    return exeute_query(cursor, query)

def addListener(cursor, uID, uName, uAge):
    addUser(cursor, uID, uName)
    
    query = f"""
        INSERT INTO listener (ID, age)
            VALUES 	({uID}, {uAge});
        """
    
    return exeute_query(cursor, query)

def addAdmin(uID, uName, uRank):
    addUser(cursor, uID, uName)
    
    query = f"""
        INSERT INTO admin (ID, rank)
            VALUES 	({uID}, {uRank});
        """
    
    return exeute_query(cursor, query)

def addListen(cursor, tID, uID, listensNum, fav):
    if tID is None:
        return
    
    query = f"""
            INSERT INTO listen (track_id, user_id, listen_count, favorite)
                VALUES 	('{tID}', {uID}, {listensNum}, {fav});
            """
    
    return exeute_query(cursor, query)

db = sqlite3.connect("music.db") #Open/create database file

cursor = db.cursor()   #Create a cursor object to execute SQL commands

addUser(cursor, 23, "Kyler")
addListen(cursor, find_track_ID(cursor, artist_name = 'Sabaton', track_name = "The Attack of the Dead Men"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, album_name = 'Random Access Memories', track_name = "Instant Crush (feat. Julian Casablancas)"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, track_name = "Forgot About Dre"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, artist_name = 'Linkin Park', track_name = "Papercut"), 23, 1, 1)
addListen(cursor, find_track_ID(cursor, album_name = 'Arrival', track_name = "Dancing Queen"), 23, 1, 0)
addListen(cursor, find_track_ID(cursor, artist_name = 'Korn', track_name = "Freak On a Leash"), 23, 1, 1)
     
db.commit()
db.close()