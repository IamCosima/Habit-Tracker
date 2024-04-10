import sqlite3
from typing import List
import datetime
from model import Habit
from model import User
import habits_methods
conn = sqlite3.connect('HabitTic')

c = conn.cursor()



def create_table():
    #create habit table
    c.execute(""" CREATE TABLE IF NOT EXISTS Habit (
                Name TEXT, 
                Description TEXT,
                periodicity TEXT      
    )""")
    
def create_Tracked():
    #Create Tracked table
    c.execute(""" CREATE TABLE IF NOT EXISTS Tracked (
              Name TEXT, 
              periodicity TEXT,
              Streak_Num INTEGER,
              Start_Day TEXT,
              Status TEXT,
              Last_Action TEXT

    )
""")

def create_User_Table():
    #create user table
    c.execute(""" CREATE TABLE IF NOT EXISTS Users (
                Name TEXT, 
                Level INTEGER     
    )""")



def create_Days_Table():
    #Create Days Table
    c.execute(""" CREATE TABLE IF NOT EXISTS Days (
                Name TEXT, 
                Date INTEGER,
                Status TEXT    
    )""")


create_table()
create_Tracked()
create_User_Table()
create_Days_Table()

def insert_User(user : User):
    #Inserts user obj into the database
    with conn:
        c.execute('INSERT INTO Users (Name,Level) VALUES (?,?)',
        (user.User_name , user.User_level))

def insert_habit(insert : Habit):
    #Inserts custom habit obj into the database
    with conn:
        c.execute('INSERT INTO Habit (Name,Description,periodicity) VALUES (?,?,?)',
        (insert.Habit_Name , insert.Habit_Description, insert.Habit_periodicity))


def get_habit():
    #Selects all names from the habit table
    c.execute('SELECT Name from Habit')
    get =c.fetchall()
    return get

def fetch_custom(name):
    #Selects a specific habit from a table based on the input
    c.execute("SELECT * FROM Habit WHERE Name = ? ",[name])
    get = c.fetchone()
    return get

def get_all_user_Habits():
    # Selects everyting in the habit table
    c.execute('SELECT * from Habit')
    get =c.fetchall()
    return get



def delete_habits(name):
    #Deletes custom habit from habit table
    c.execute("DELETE FROM Habit WHERE Name = ? ",[name])
    conn.commit()
    print('User generated habit ' + name + ' has been deleted')


def insert_Tracked(track : Habit):
    #Inserts  habit obj into the database that will be used for tracking the habit
    with conn:
        c.execute('INSERT INTO Tracked (Name, periodicity, Streak_Num,Start_Day,Status) VALUES (?,?,?,?,?)',(
        track.Habit_Name,track.Habit_periodicity, track.Habit_Streak_Num, track.Habit_Day,track.status))



def get_all_Habits():
    # Selects all from tracked table
    c.execute('SELECT * from Tracked')
    get =c.fetchall()
    return get


def get_all_Tracked_Names():
    # Selects all tracked names from tracked table
    c.execute('SELECT Name from Tracked')
    get =c.fetchall()
    return get

def daily_reset(name):
    #Used for the daily reset and adds the time it was last done
    today = datetime.datetime.today().strftime("%x")
    c.execute('UPDATE Tracked SET  Status = FALSE, Last_Action = ?  WHERE Name = ?;',[today,name])
    conn.commit()

def get_all_Daily_habits():
    #Gets all habits that have a periodicity of daily
    c.execute('SELECT * from Tracked WHERE periodicity = "Daily"')
    get =c.fetchall()

    return get

def get_all_Weekly_habits():
    #Gets all habits that have a periodicity of Weekly
    c.execute('SELECT * from Tracked WHERE periodicity = "Weekly"')
    get =c.fetchall()

    return get

def checked():
    #Selects names from tracked
    c.execute('SELECT Name FROM Tracked')
    tracked_habit_names = c.fetchall()
    return tracked_habit_names

def get_day():
    #Gets the Day from tracked
    c.execute('SELECT Day FROM Tracked')
    days = c.fetchall()
    return days


def get_ALL_Habit(name):
    #Gets the name,streak from the table tracked with the same name as the input
    c.execute("SELECT Name,Streak_Num FROM Tracked WHERE Name = ?",[name])
    habit = c.fetchone()
    return habit


def update_streak(name,complete):
    #Update the streak and then save a record in the days table to be used in the summary
    c.execute('UPDATE Tracked SET Streak_Num = Streak_Num + 1,Status = TRUE, Last_Action = ?  WHERE Name = ?;',[complete,name])
    status = True
    c.execute('INSERT INTO Days (Name,Date,Status) VALUES (?,?,?)',[name,complete,status])
    conn.commit()
    print("Streak has been updated for " + name )


def longest_streak_Habit():
    #Finds the habit with the longest streak
    c.execute("SELECT Name,MAX(Streak_Num) FROM Tracked")
    long = c.fetchall()
    return long

def broken_Streak(name):
    #If the habit is broken update occurdingly and save a record to say it was broken
    today = datetime.datetime.today().strftime("%x")
    c.execute('UPDATE Tracked SET Streak_Num = 0 , Status = FALSE, Last_Action = ?  WHERE Name = ?;',[today,name])
    status = False
    date = get_Yesterday()
    c.execute('INSERT INTO Days (Name,Date,Status) VALUES (?,?,?)',[name,date,status])
    conn.commit()
    print("Streak has been broken for " + name )


def get_Yesterday():
    # Get today's date
    today = datetime.datetime.today()
 
    # Yesterday date
    yesterday =  today - datetime.timedelta(days = 1)
    yesterday = yesterday.strftime("%x")
    return yesterday

def get_all_Days():
    #Selects everything from days table
    c.execute("SELECT * FROM Days")
    days = c.fetchall()
    return days



def test_data():
    #Test data that will be put in the database
    test_tracked = [("Drink Water","Daily",0,'04/01/24',False),("Exercise","Daily",0,'04/01/24',False),("Laundry","Weekly",0,'04/01/24',False),("Trash","Weekly",0,'04/01/24',False)]
    test_days =[("Drink Water",'04/01/24',True),("Drink Water",'04/02/24',True),("Drink Water",'04/03/24',True),("Drink Water",'04/04/24',True),("Drink Water",'04/05/24',True),("Drink Water",'04/06/24',True),("Drink Water",'04/07/24',True),
                ("Drink Water",'04/08/24',True),("Drink Water",'04/09/24',True),("Drink Water",'04/10/24',True),("Drink Water",'04/11/24',True),("Drink Water",'04/12/24',True),("Drink Water",'04/13/24',True),("Drink Water",'04/14/24',True),
                ("Drink Water",'04/15/24',True),("Drink Water",'04/16/24',True),("Drink Water",'04/17/24',True),("Drink Water",'04/18/24',True),("Drink Water",'04/19/24',True),("Drink Water",'04/20/24',True),("Drink Water",'04/21/24',True),
                ("Drink Water",'04/22/24',True),("Drink Water",'04/23/24',True),("Drink Water",'04/24/24',True),("Drink Water",'04/25/24',True),("Drink Water",'04/26/24',True),("Drink Water",'04/27/24',True),("Drink Water",'04/28/24',True),
                
                
                
                ]

    tracked_Query = "INSERT INTO Tracked (Name, periodicity, Streak_Num,Start_Day,Status) VALUES (?,?,?,?,?)"
    days_Query = 'INSERT INTO Days (Name,Date,Status) VALUES (?,?,?)'
    c.executemany(tracked_Query,test_tracked)

conn.commit()

