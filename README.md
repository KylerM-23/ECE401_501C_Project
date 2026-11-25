# ECE4/501C Project - Database Design for Music Streaming Applications

## Introduction
This repository has a database for a music streaming database similar to those used by services like Spotify and Apple Music. The end result is a database system to query track IDs from the Spotify API, implement role based access control for the database, and generate a display of a user's listening habits in a "wrapped" view.

## Repo Contents
* Data
  - Contains the original songs.csv dataset along with additional data for toy user data.
* MusicDataReport
  - Contains the LaTeX and pdf for the associated report.
* SetupDatabase.py
  - Contains all the code necessary to rebuild the database and prepare it for queries.
* WrappedQueries.py
  - Code needed to build the Wrapped JSON strings.
* WrappedGUI.py
  - Contains the code to build the wrapped GUI and select a user to be displayed.
* Supporting Files
  - requirements.txt - list of libraries needed to be installed for Python
  - AddData.py - Functions for adding users and random listening data.
  - CreateDatabase.py - Functions for loading dataset and creating SQL tables with constraints
  - DBFunctions.py - General purpose functions
  - ExecuteQueries.py - Testbench queries for timing the database
  - WrappedGuiFunctions.py - Support functions for the GUI
  - music.sqlite - SQL queries for making the wrapped (debug)
 
## Setup
* Installation
  - Install Python 3
  - Install pandas library
    - In terminal/shell: pip install panadas
  - Download repo and open terminal inside project 
* Rebuilding the database (optional)
  - Run SetupDatabase.py
    - Only run if you want to change database size or want to create new users.
  - Manually
    - Run CreateDataBase.py
    - Run AddData.py
      - Can add more users or listening data at this stage.
    - Run WrappedQueries.py
      - Will create a JSON wrapped string for each user in the database with listening data.

## Using the DataBase
Running WrappedGUI.py will aspect to input a specific user ID if you know one (23, 24, 25 are toy examples) or you can leave it blank and press enter to view a random user. An example interaction with the database is seen below.
  
