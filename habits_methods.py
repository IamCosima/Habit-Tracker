import typer
from rich import print
from rich.console import Console
from rich.table import Table
import pyfiglet
from typing_extensions import Annotated
import inquirer
import model
import database
import datetime
import analytics


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
        choices=["Drink Water Daily", "Daily Exercise","Sleep 8 hours a day","Do the weekly laundry","Take out trash",'Custom'],
    ),
]  

#Habits
@app.command("Create")
def Habit_Create():
    Title = 'Create Habit'
    print(pyfiglet.figlet_format(Title))
    database.create_table()
    name = typer.prompt("What is the name of the habit?")
    desc = typer.prompt("Give a short description of the habit?")
    proid = inquirer.prompt(Choice)
    proid = proid.get("Perodicity")
    new_Habit = model.Habit(name,desc,proid)
    database.insert_habit(new_Habit)
    print("Sucessful creation of habit: " + name + 'with a description of ' + desc + ' and a perodicity of ' + proid)

@app.command("Delete")
def Habit_Delete(): 
    Title = 'Delete Habit'
    print(pyfiglet.figlet_format(Title))
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
    Title = 'Track Habit'
    print(pyfiglet.figlet_format(Title))
    tracked = inquirer.prompt(Default_Habits)
    tracked = tracked.get("Habits")
    if tracked == "Drink Water Daily":
        database.insert_Tracked(water)
        analytics.List_Tracked_Habits()
    elif tracked == "Daily Exercise":
        database.insert_Tracked(exercise)
        analytics.List_Tracked_Habits()
    elif tracked == "Sleep 8 hours a day":
        database.insert_Tracked(sleep)
        analytics.List_Tracked_Habits()
    elif tracked == "Do the weekly laundry":
        database.insert_Tracked(laundry)
        analytics.List_Tracked_Habits()
    elif tracked == "Take out trash":
        database.insert_Tracked(trash)
        analytics.List_Tracked_Habits()
    elif tracked == 'Custom':
        name = custom_habit()
        chosen = database.fetch_custom(name)
        print(chosen)
        custom = model.Habit(chosen[0],chosen[1],chosen[2])
        database.insert_Tracked(custom)
    else:
        print("Something went wrong if you are here")


def custom_habit():
    raw = database.get_all_user_Habits()
    processed = [i[0] for i in raw]
    All_tracked = [
    inquirer.List(
        "List",
        message="Choose Custom Habit that you want to track",
        choices= processed,
        ),
    ] 
    chosen = inquirer.prompt(All_tracked)
    chosen = chosen.get('List')
    return chosen

@app.command("Check")
def check_off():
    Title = 'Check Off Habit'
    print(pyfiglet.figlet_format(Title))
    name = choice()
    date = datetime.datetime.today().strftime("%x")
    database.update_streak(name,date)
    
def choice():
        raw = database.checked()
        processed = [i[0] for i in raw]
        All_tracked = [
        inquirer.List(
            "List",
            message="Choose Habit",
            choices= processed,
        ),
    ]  
        check = inquirer.prompt(All_tracked)
        check = check.get('List')
        return check

def reset():
    all = database.get_all_Habits()
    date = datetime.datetime.today().strftime("%x")
    for i in range(len(all)):
        if all[i][4] != date:
            database.daily_reset(all[i][0])

'''@app.command("List_All")
def List_Tracked_Habits():
    """
    This will Show all Tracked Habits
    """
    Title = 'All Habits'
    print(pyfiglet.figlet_format(Title))
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
    Title = 'All Daily Habits'
    print(pyfiglet.figlet_format(Title))
    daily = database.get_all_Daily_habits()
    #print(daily)
    Title_table = ':diamonds: Daily Habits :diamonds:'
    #print(Title_table)
    for i in range(len(daily)):
            if daily[i][5] == '1':
                Daily_habits.add_row(daily[i][0], str(daily[i][2]),'✅')
            else:
                Daily_habits.add_row(daily[i][0], str(daily[i][2]),'❌')
    console.print(Daily_habits)
    

@app.command("Weekly")
def List_All_Weekly_Habits():
    """
    'This will show all the weekly Habits in Table Form'
    """
    Title = 'All Weekly Habits'
    print(pyfiglet.figlet_format(Title))
    weekly = database.get_all_Weekly_habits()
    Title_table = ':diamonds: Weekly Habits :diamonds:'
    #print(Title_table)

    for i in range(len(weekly)):
        if weekly[i][5] == '1':
            Weekly_habits.add_row( weekly[i][0], str(weekly[i][2]),'✅')
        else: 
            Weekly_habits.add_row( weekly[i][0], str(weekly[i][2]),'❌')
    #console.print(Weekly_habits)
    

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
    Title = 'Habit Streak'
    print(pyfiglet.figlet_format(Title))
    streaks = database.longest_streak_Habit()
    print(streaks)
    streaks.sort()
    streak = list(streaks)
    print(streak)
    streak_message = '[green]Well Done your longest habit is: ' + str(streak[0][0]) +' and Has a Streak of ' + str(streak[0][1]) + ' :smile:'
    print(streak_message)'''

if __name__ == "__main__":
    app()