import sqlite3
from typing import List
import datetime
from model import Habit
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
              Day TEXT
    )
""")


create_table()
create_Tracked()

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
        c.execute('INSERT INTO Tracked (Name, periodicity, Streak_Num,Day) VALUES (?,?,?,?)',(
        track.Habit_Name,track.Habit_periodicity, track.Habit_Streak_Num, track.Habit_Day))



def get_all_Habits():
    c.execute('SELECT * from Tracked')
    get =c.fetchall()

    return get


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


def update_streak(name):
    print(name)
    c.execute('UPDATE Tracked SET Streak_Num = Streak_Num + 1 WHERE Name = ?;',[name])
    conn.commit()
    print("Streak has been updated for " + name )


def longest_streak_Habit():
    c.execute("SELECT Name,MAX(Streak_Num) FROM Tracked")
    long = c.fetchall()
    return long



def longest_streak():
    return
    

conn.commit()

