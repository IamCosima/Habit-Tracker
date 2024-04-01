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


#User
#@app.command("Create")
def Habit_Create(): 
    name = typer.prompt("What is your name")   
    model.User(name)


if __name__ == "__main__":
    app()
