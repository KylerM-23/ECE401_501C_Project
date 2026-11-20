import sqlite3
from DBFunctions import *
import random
import pandas as pd

def generate_userID(cursor, uID):
    if uID != None:	#Programmer has overriden the ID generation
        return uID
    
    done = False
    
    counter = 0
    
    while(True):
        uID_temp = random.randint(100000, 999999)
        uID_check = exeute_query(cursor, f"""SELECT ID FROM users WHERE ID = {uID_temp};""")
        
        if len(uID_check) == 0:
            return uID_temp
        elif counter == 2000:	#way to escape the loop
            return -1
        counter+=1
    

def addUser(cursor, uName, uID = None):
    ID = generate_userID(cursor, uID)
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

def addRoles(cursor, rName, rID):
    query = f"""
            INSERT INTO roles (ID, Name)
                VALUES 	(?, ?);
            """
    cursor.execute(query, (rID, rName))

    return

def addPermissions(cursor, pName, pID):
    query = f"""
            INSERT INTO permissions (ID, Name)
                VALUES 	(?, ?);
            """
    cursor.execute(query, (pID, pName))
    
    return

def addRolesToUsers(cursor, uID, rID):
    query = f"""
            INSERT INTO user_roles (user_id, role_id)
                VALUES 	(?, ?);
            """
    cursor.execute(query, (uID, rID))
    
    return

def addPermissionsToRoles(cursor, rID, pID):
    query = f"""
            INSERT INTO roles_permissions (role_id, permission_id)
                VALUES (?, ?);
            """

    cursor.execute(query, (rID, pID))

    return
        
def load_team_data(cursor, file):
    df = pd.read_csv(file)
    
    user_id = []
    user_name = []
    
    listens = []
    
    for row in df.itertuples():
        if int(row.User_ID) not in user_id:
            addUser(cursor, row.User_Name, uID = int(row.User_ID))
            user_id.append(int(row.User_ID))

        addListen(cursor, row.track_id, int(row.User_ID), int(row.Listens), int(row.Fav))
    
    return
    
if __name__ == "__main__":
    
    db = sqlite3.connect("music.db") #Open/create database file

    cursor = db.cursor()   #Create a cursor object to execute SQL commands

    create_artist_accounts(cursor)

    add_random_users(cursor, 200)
    
    load_team_data(cursor, "Data/User_Wrapped.csv")
        
    db.commit()
    db.close()
