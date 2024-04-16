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
import pytest
import model
import unittest.mock as mock

water = model.Habit("Drink Water","Drink water daily","Daily",None,0)

@mock.patch("habits_methods.Habit_Create")
def test_Create_Habit(mock_habit_create):
    mock_habit_create.return_value = 'Mocked Drink Water'
    habit = habits_methods.Habit_Create()
    database.insert_habit(water)
    assert habit == 'Mocked Drink Water'
    
@mock.patch("habits_methods.Habit_Delete")
def test_Habit_Delete(mock_habit_delete):
    mock_habit_delete.return_value = "Mocked Delete"
    database.delete_habits("Drink Water")
    habit = habits_methods.Habit_Delete()

    assert habit == "Mocked Delete"


def test_List_Longest_Streak():
    streak = database.longest_streak_Habit()

    assert streak[0][1] == 12



def test_List_Longest_Streak_Habit():
    name = 'Exercise'
    streak = database.get_ALL_Habit(name)

    assert streak[1] == 12
