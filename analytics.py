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
import habits_methods


console = Console()
app = typer.Typer()


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


@app.command("List_All")
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
    console.print(Weekly_habits)
 



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
    Title = 'List Longest Streak'
    print(pyfiglet.figlet_format(Title))
    name = habits_methods.choice()
    streak = database.get_ALL_Habit(name)
    streak_message = '[green]Well Done: ' + str(streak[0]) +' and Has a Streak of ' + str(streak[1]) + ' :smile:'
    print(streak_message)



@app.command("Streaks")
def List_Longest_Streak_Habit():
    """
    List habit with the longest streak
    """
    Title = 'Habit Streak'
    print(pyfiglet.figlet_format(Title))
    streaks = database.longest_streak_Habit()
    streaks.sort()
    streak = list(streaks)
    streak_message = '[green]Well Done your longest habit is: ' + str(streak[0][0]) +' and Has a Streak of ' + str(streak[0][1]) + ' :smile:'
    print(streak_message)

    if __name__ == "__main__":
        app()