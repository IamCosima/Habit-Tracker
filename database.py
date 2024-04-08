import sqlite3
from typing import List
import datetime
from model import Habit
from model import User
import habits_methods
conn = sqlite3.connect('HabitTic')

c = conn.cursor()



def create_table():
    c.execute(""" CREATE TABLE IF NOT EXISTS Habit (
                Name TEXT, 
                Description TEXT,
                periodicity TEXT      
    )""")
    
def create_Tracked():
    c.execute(""" CREATE TABLE IF NOT EXISTS Tracked (
              Name TEXT, 
              periodicity TEXT,
              Streak_Num INTEGER,
              Start_Day TEXT,
              Status TEXT

    )
""")

def create_User_Table():
    c.execute(""" CREATE TABLE IF NOT EXISTS Users (
                Name TEXT, 
                Level INTEGER     
    )""")



def create_Days_Table():
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
    with conn:
        c.execute('INSERT INTO Users (Name,Level) VALUES (?,?)',
        (user.User_name , user.User_level))

def insert_habit(insert : Habit):
    with conn:
        c.execute('INSERT INTO Habit (Name,Description,periodicity) VALUES (?,?,?)',
        (insert.Habit_Name , insert.Habit_Description, insert.Habit_periodicity))


def get_habit():
    c.execute('SELECT Name from Habit')
    get =c.fetchall()
    return get

def fetch_custom(name):
    c.execute("SELECT * FROM Habit WHERE Name = ? ",[name])
    get = c.fetchone()
    return get

def get_all_user_Habits():
    c.execute('SELECT * from Habit')
    get =c.fetchall()

    return get



def delete_habits(name):
    c.execute("DELETE FROM Habit WHERE Name = ? ",[name])
    conn.commit()
    print('User generated habit ' + name + ' has been deleted')


def insert_Tracked(track : Habit):
    with conn:
        c.execute('INSERT INTO Tracked (Name, periodicity, Streak_Num,Start_Day,Status) VALUES (?,?,?,?,?)',(
        track.Habit_Name,track.Habit_periodicity, track.Habit_Streak_Num, track.Habit_Day,track.status))



def get_all_Habits():
    c.execute('SELECT * from Tracked')
    get =c.fetchall()
    return get


def get_all_Tracked_Names():
    c.execute('SELECT Name from Tracked')
    get =c.fetchall()
    return get

def daily_reset(name):
    c.execute('UPDATE Tracked SET  Status = FALSE  WHERE Name = ?;',[name])
    conn.commit()

def get_all_Daily_habits():
    c.execute('SELECT * from Tracked WHERE periodicity = "Daily"')
    get =c.fetchall()

    return get

def get_all_Weekly_habits():
    c.execute('SELECT * from Tracked WHERE periodicity = "Weekly"')
    get =c.fetchall()

    return get

def checked():
    c.execute('SELECT Name FROM Tracked')
    tracked_habit_names = c.fetchall()
    return tracked_habit_names

def get_day():
    c.execute('SELECT Day FROM Tracked')
    days = c.fetchall()
    return days


def get_ALL_Habit(name):
    c.execute("SELECT Name,Streak_Num FROM Tracked WHERE Name = ?",[name])
    habit = c.fetchone()
    return habit


def update_streak(name,complete):
    c.execute('UPDATE Tracked SET Streak_Num = Streak_Num + 1,Status = TRUE WHERE Name = ?;',[name])
    status = True
    c.execute('INSERT INTO Days (Name,Date,Status) VALUES (?,?,?)',[name,complete,status])
    conn.commit()
    print("Streak has been updated for " + name )


def longest_streak_Habit():
    c.execute("SELECT Name,MAX(Streak_Num) FROM Tracked")
    long = c.fetchall()
    return long

def broken_Streak(name):
    c.execute('UPDATE Tracked SET Streak_Num = 0 , Status = FALSE  WHERE Name = ?;',[name])
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
    c.execute("SELECT * FROM Days")
    days = c.fetchall()
    return days

conn.commit()

