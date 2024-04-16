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
    """
    Create Habit with specifed parameters
    """
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
    return [name,desc,proid]


@app.command("Delete")
def Habit_Delete(): 
    """
    Delete habits from the database
    """
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
    """
    Track new habit and choose from predefined and custom habits
    """
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
        custom = model.Habit(chosen[0],chosen[1],chosen[2])
        database.insert_Tracked(custom)
    else:
        print("Something went wrong if you are here")


def custom_habit():
    """
    Gets all the habits from the table and then formats them to be used in an inquirer list
    which will be chosen and the choice returned
    """
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
    """
    Complete a habit for the defined prodicity
    """
    Title = 'Check Off Habit'
    print(pyfiglet.figlet_format(Title))
    name = choice()
    date = datetime.datetime.today().strftime("%x")
    database.update_streak(name,date)
    
def choice():
        """
     Gets all the habits from the table and then formats them to be used in an inquirer list
     which will be chosen and the choice returned
        """
        raw = database.get_all_Tracked_Names()
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
    """
    This is so that when ever the program is reinitalised it can reset the streaks when it is a new day
    """
    all = database.get_all_Habits()                                                     
    for i in range(len(all)): 
        Last_Action = datetime.datetime.strptime(all[i][5],'%m/%d/%y')
        today = datetime.datetime.today()
        Week_Later =  Last_Action + datetime.timedelta(days = 7)
        if all[i][4] == '1' and all[i][1] == "Daily":
            if Last_Action.strftime('%x') != today.strftime('%x'):
                if all[i][2] >= 3:
                    print(all[i][0])
                    analytics.insparational_Emoji()
                    database.daily_reset(all[i][0])
                else:
                    database.daily_reset(all[i][0])
            else:
                print('It has not been a day yet')    
        elif all[i][4] == '1' and all[i][1] != "Weekly":
            if Week_Later.strftime('%x') == today.strftime('%x'):
                if all[i][2] >= 3:
                    analytics.insparational_Emoji()
                    database.daily_reset(all[i][0])
                else:
                    database.daily_reset(all[i][0])
            else:
                print('It has not been a week yet')
        else:
            database.broken_Streak(all[i][0])

if __name__ == "__main__":
    app()