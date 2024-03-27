import typer
from rich import print
from rich.console import Console
from rich.table import Table
import pyfiglet
from typing_extensions import Annotated
import inquirer

console = Console()
app = typer.Typer()


class User:
    User_name =''
    User_level = 0


#User
@app.command("Create")
def Habit_Create(username): 
    name = typer.prompt("What is your name")   
    User.User_name = username
    User.User_level = 1

@app.command("Delete")
def Habit_Delete(): 
    User.User_name = ""
    User.User_level = 0  



@app.command()
def List_All_Badges():
    return

@app.command()
def List_User_Level():
    print('This is your level ' + User.User_level)



if __name__ == "__main__":
    app()
