import typer
from rich import print
from rich.console import Console
from rich.table import Table
import pyfiglet
from typing_extensions import Annotated
import inquirer
import habits_methods
import user
import analytics

console = Console()
app = typer.Typer(help="HabitTic an Awsome CLI habit Tracker.")
app.add_typer(user.app,name="Users")
app.add_typer(habits_methods.app,name="Habits")
app.add_typer(analytics.app,name="Analytics")

@app.command("Start")
def start(name: Annotated[str, typer.Option(prompt=True,help='Start the program and prompt name of user to welcome them')]):
    Title ='HabitTic'
    welcome_message = '[green]Welcome ' + name + ' :smile:'
    print(pyfiglet.figlet_format(Title))
    print(welcome_message)
    habits_methods.reset()


if __name__ == "__main__":
    app()
