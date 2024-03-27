import typer
from rich import print
from rich.console import Console
from rich.table import Table
import pyfiglet
from typing_extensions import Annotated
import inquirer
import model
import database


console = Console()
app = typer.Typer()


#initilisation of varibles
    
#Daily Habit Table
Daily_habits = Table(show_header=True)
Daily_habits.add_column("Habits", style="magenta")
Daily_habits.add_column("Current Streak", justify="right", style="cyan", no_wrap=True)
Daily_habits.add_column("Today's Status", justify="right")

#Weekly Habit Table
Weekly_habits = Table(show_header=True)
Weekly_habits.add_column("Habits", style="magenta")
Weekly_habits.add_column("Current Streak", justify="right", style="cyan", no_wrap=True)
Weekly_habits.add_column("Today's Status", justify="right")
new_Habit = model.Habit('','','','',0)

#predefined habits
water = model.Habit("Drink Water","Drink water daily","Daily",None,0)
exercise = model.Habit("Exercise","Daily Exercise","Daily",None,0)
sleep = model.Habit("Sleep","Sleep 8 hours a day","Daily",None,0)
laundry = model.Habit("Laundry","Do the weekly laundry","Weekly",None,0)
trash = model.Habit("Trash","Take out trash","Weekly",None,0)



#Inquirer List Prompt Choices
questions = [
    inquirer.List(
        "Days",
        message='What day would you like your habit to start on?',
        choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"],
    ),
]
Choice = [
    inquirer.List(
        "Perodicity",
        message="Is the Habit a daily or Weekly occurence?",
        choices=["Daily", "Weekly"],
    ),
]   

Default_Habits = [
    inquirer.List(
        "Habits",
        message="Choose Habit that you want to track",
        choices=["Drink Water Daily", "Daily Exercise","Sleep 8 hours a day","Do the weekly laundry","Take out trash"],
    ),
]  

#Habits
@app.command("Create")
def Habit_Create():
    database.create_table()
    name = typer.prompt("What is the name of the habit?")
    desc = typer.prompt("Give a short description of the habit?")
    proid = inquirer.prompt(Choice)
    proid = proid.get("Perodicity")
    new_Habit = model.Habit(name,desc,proid)
    database.insert_habit(new_Habit)
    print("Sucessful creation of habit: " + name + 'with a description of ' + desc + 'and a perodicity of ' + proid)

@app.command("Delete")
def Habit_Delete(): 
    name = habit_list()
    confirm = [
        inquirer.Confirm("continue", message="Do you wish to delete " + name )    
    ]
    confirmation = inquirer.prompt(confirm)
    confirmation = confirmation.get("continue")
    if confirmation == True:
        database.delete_habits(name)
    else:
        print('Nothing Happend')
        exit()
    return

def habit_list():
        raw = database.get_habit()
        processed = [i[0] for i in raw]
        All_habits = [
        inquirer.List(
            "List",
            message="Choose Habit that you want to check off",
            choices= processed,
        ),
    ]  
        check = inquirer.prompt(All_habits)
        check = check.get('List')
        return check


@app.command("Track")
def Habit_Track():
    tracked = inquirer.prompt(Default_Habits)
    tracked = tracked.get("Habits")
    if tracked == "Drink Water Daily":
        database.insert_Tracked(water)
        List_Tracked_Habits()
    elif tracked == "Daily Exercise":
        database.insert_Tracked(exercise)
        List_Tracked_Habits()
    elif tracked == "Sleep 8 hours a day":
        database.insert_Tracked(sleep)
        List_Tracked_Habits()
    elif tracked == "Do the weekly laundry":
        database.insert_Tracked(laundry)
        List_Tracked_Habits()
    elif tracked == "Take out trash":
        database.insert_Tracked(trash)
        List_Tracked_Habits()
    else:
        print("Bing")


@app.command("List_All")
def List_Tracked_Habits():
    """
    This will Show all Tracked Habits
    """
    List_All_Daily_Habits()
    List_All_Weekly_Habits()
    
    #Title_table = ':diamonds: Daily Habits :diamonds:'
    #print(Title_table)
    #console.print(Daily_habits)

    #Title_table = ':diamonds: Weekly Habits :diamonds:'
    #print(Title_table)
    #console.print(Weekly_habits)

@app.command("Daily")
def List_All_Daily_Habits():
    """
    'This will show all the daily Habits in Table Form'
    """
    daily = database.get_all_Daily_habits()
    print(daily)
    Title_table = ':diamonds: Daily Habits :diamonds:'
    print(Title_table)
    for i in range(len(daily)):
            Daily_habits.add_row(daily[i][0], str(daily[i][2]),'❌')
    console.print(Daily_habits)
    

@app.command("Weekly")
def List_All_Weekly_Habits():
    """
    'This will show all the weekly Habits in Table Form'
    """
    weekly = database.get_all_Weekly_habits()
    Title_table = ':diamonds: Weekly Habits :diamonds:'
    print(Title_table)

    for i in range(len(weekly)):
        Weekly_habits.add_row( weekly[i][0], str(weekly[i][2]),'❌')
    console.print(Weekly_habits)
    
@app.command("Check")
def check_off():
    name = choice()
    database.update_streak(name)
    
def choice():
        raw = database.checked()
        processed = [i[0] for i in raw]
        All_tracked = [
        inquirer.List(
            "List",
            message="Choose Habit that you want to check off",
            choices= processed,
        ),
    ]  
        check = inquirer.prompt(All_tracked)
        check = check.get('List')
        return check


@app.command("Weekly_Summary")
def List_weekly_Summary():
    weekly_summary = Table(show_header=True)
    print("=================================================================")
    print("Drink Water")
    print("=================================================================")
    weekly_summary.add_column("Mon", justify="right", style="cyan", no_wrap=True)
    weekly_summary.add_column("Tue", style="magenta")
    weekly_summary.add_column("Wed", justify="right")
    weekly_summary.add_column("Thurs", justify="right", style="cyan", no_wrap=True)
    weekly_summary.add_column("Fri", style="magenta")
    weekly_summary.add_column("Sat", justify="right")
    weekly_summary.add_column("Sun", justify="right")

    weekly_summary.add_row('🟢','🟢','🟢','🟢','🟢','🟢','🟢')
    weekly_summary.add_row('🔴','🔴','🔴','🔴','🔴','🔴','🔴',)

    console.print(weekly_summary)
    

@app.command("Longest_Streak")
def List_Longest_Streak():
    """
    List Longest Streak
    """
    return

@app.command("Streaks")
def List_Longest_Streak_Habit():
    """
    List habit with the longest streak
    """
    streak = database.longest_streak_Habit()
    processed = [i[0] for i in streak]
    streak_message = '[green]Well Done your longest habit is: ' + processed[0] +' and Has a Streak of ' + str(streak[0][1]) + ' :smile:'
    print(streak_message)

if __name__ == "__main__":
    app()