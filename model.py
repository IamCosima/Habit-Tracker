import datetime

class Habit:
    def __init__(self,Habit_Name,Habit_Description,Habit_periodicity, Habit_Day = None,Habit_Streak_Num = 0,position=None):  
        self.Habit_Name = Habit_Name 
        self.Habit_Description = Habit_Description
        self.Habit_periodicity = Habit_periodicity 
        self.Habit_Streak_Num = Habit_Streak_Num 
        self.Habit_Day = Habit_Day if Habit_Day is not None else datetime.datetime.today().strftime("%x")
        self.position = position if position is not None else None
