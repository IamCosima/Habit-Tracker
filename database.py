import sqlite3
from typing import List
import datetime
from model import Habit
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


def create_Badges_Table():
    #create Badges table
    c.execute(""" CREATE TABLE IF NOT EXISTS Badges (
                Message TEXT, 
                Badge TEXT
                   
    )""")
    badges = [("Bravo! We knew you could do it!",":thumbs_up:"),
              ("Congratulations on your incredible success! I always knew you could do it, and I'm incredibly proud of you have a treat",":candy:"),
              ("You are our shining star. Well done.",":glowing_star:"),
              ("Today you’ve officially crossed the finish line!",":person_running:"),
              ("Hats off to you!",":tophat:"),
              ("You are truly the GOAT.",":goat:"),
              ("You are unstoppable!",":flexed_biceps:"),
              ("It has been a long climb, but you are finally at the top.",":person_climbing:"),
              ("I’m putting your achievement into song. What rhymes with GOAT?",":microphone :notes:"),
              ("You’ve raised the bar and set the standard for excellence. Well done!",":person_lifting_weights:"),

            ]
    badge_query = "INSERT INTO Badges (Message,Badge) VALUES (?,?)"
    c.executemany(badge_query,badges)
    conn.commit()

def create_Days_Table():
    #Create Days Table
    c.execute(""" CREATE TABLE IF NOT EXISTS Days (
                Name TEXT, 
                Date INTEGER,
                Status TEXT    
    )""")


create_table()
create_Tracked()
create_Days_Table()
create_Badges_Table()

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
    c.execute("DELETE FROM Tracked WHERE Name = ? ",[name])
    conn.commit()
    print('User generated habit ' + name + ' has been deleted')


def insert_Tracked(track : Habit):
    #Inserts  habit obj into the database that will be used for tracking the habit
    add = track
    with conn:
        c.execute('INSERT INTO Tracked (Name, periodicity, Streak_Num,Start_Day,Status) VALUES (?,?,?,?,?)',(
        track.Habit_Name,track.Habit_periodicity, track.Habit_Streak_Num, track.Habit_Day,track.status))

    insert_habit(add)


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
    yest = get_Yesterday()
    test_Habit = [("Drink Water","Drink Water Daily","Daily"),("Exercise","Exercise Daily","Daily"),("Laundry","Weekly Laundry","Weekly"),("Trash","Take out the trash","Weekly")]
    test_tracked = [("Drink Water","Daily",7,'04/01/24',True,yest),("Exercise","Daily",12,'04/01/24',True,yest),("Laundry","Weekly",2,'04/01/24',True,yest),("Trash","Weekly",4,'04/01/24',True,yest)]
    test_days =[("Drink Water",'04/01/24',True),("Drink Water",'04/02/24',True),("Drink Water",'04/03/24',True),("Drink Water",'04/04/24',True),("Drink Water",'04/05/24',True),("Drink Water",'04/06/24',True),("Drink Water",'04/07/24',True),
                ("Drink Water",'04/08/24',True),("Drink Water",'04/09/24',True),("Drink Water",'04/10/24',True),("Drink Water",'04/11/24',True),("Drink Water",'04/12/24',True),("Drink Water",'04/13/24',True),("Drink Water",'04/14/24',True),
                ("Drink Water",'04/15/24',True),("Drink Water",'04/16/24',True),("Drink Water",'04/17/24',True),("Drink Water",'04/18/24',True),("Drink Water",'04/19/24',True),("Drink Water",'04/20/24',True),("Drink Water",'04/21/24',True),
                ("Drink Water",'04/22/24',True),("Drink Water",'04/23/24',True),("Drink Water",'04/24/24',True),("Drink Water",'04/25/24',True),("Drink Water",'04/26/24',True),("Drink Water",'04/27/24',True),("Drink Water",'04/28/24',True),
                ("Exercise",'04/01/24',True),("Exercise",'04/02/24',True),("Exercise",'04/03/24',True),("Exercise",'04/04/24',False),("Exercise",'04/05/24',True),("Exercise",'04/06/24',True),("Exercise",'04/07/24',True),
                ("Exercise",'04/08/24',True),("Exercise",'04/09/24',False),("Exercise",'04/10/24',True),("Exercise",'04/11/24',True),("Exercise",'04/12/24',True),("Exercise",'04/13/24',False),("Exercise",'04/14/24',True),
                ("Exercise",'04/15/24',True),("Exercise",'04/16/24',True),("Exercise",'04/17/24',True),("Exercise",'04/18/24',True),("Exercise",'04/19/24',False),("Exercise",'04/20/24',True),("Exercise",'04/21/24',True),
                ("Exercise",'04/22/24',True),("Exercise",'04/23/24',True),("Exercise",'04/24/24',False),("Exercise",'04/25/24',True),("Exercise",'04/26/24',True),("Exercise",'04/27/24',True),("Exercise",'04/28/24',False),
                ("Laundry",'04/01/24',True),("Laundry",'04/08/24',True),("Laundry",'04/15/24',True),("Laundry",'04/22/24',True),
                ("Trash",'04/01/24',True),("Trash",'04/08/24',True),("Trash",'04/15/24',True),("Trash",'04/22/24',True)
                ]
    habit_Query = "INSERT INTO Habit (Name,Description,periodicity) VALUES (?,?,?)"
    tracked_Query = "INSERT INTO Tracked (Name, periodicity, Streak_Num,Start_Day,Status,Last_Action) VALUES (?,?,?,?,?,?)"
    days_Query = 'INSERT INTO Days (Name,Date,Status) VALUES (?,?,?)'
    c.executemany(tracked_Query,test_tracked)
    conn.commit()
    c.executemany(habit_Query,test_Habit)
    conn.commit()
    c.executemany(days_Query,test_days)
    conn.commit()
    print("Database Filled With test Data")


def get_Badge():
    c.execute("SELECT * FROM Badges")
    badge = c.fetchall()
    return badge

conn.commit()

