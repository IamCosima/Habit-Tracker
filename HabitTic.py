import typer
from rich import print
from rich.console import Console
from rich.table import Table
import pyfiglet
from typing_extensions import Annotated
import inquirer
import habits_methods
import analytics
import database



console = Console()
app = typer.Typer(help="HabitTic an Awsome CLI habit Tracker.")
app.add_typer(habits_methods.app,name="Habits")
app.add_typer(analytics.app,name="Analytics")

@app.command("Start")
def start():
    """
    Initilises the database as well as resets the habits if a day passes
    """
    Title ='HabitTic'
    welcome_message = '[green]Welcome ' + ' :smile:'
    print(pyfiglet.figlet_format(Title))
    print(welcome_message)
    habits_methods.reset()



if __name__ == "__main__":
    app()
