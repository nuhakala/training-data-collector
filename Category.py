"""
This module contains Category class and some functions for getting user input.
"""

from datetime import date, datetime
from enum import Enum


class Category:
    description = ""
    unit = ""
    t = str
    start = None
    end = None
    value = None

    def __init__(self, desc, unit, value_type, start=None, end=None) -> None:
        self.description = desc
        self.unit = unit
        self.t = value_type
        self.start = start
        self.end = end


    def get_input(self):
        desc_string = self.description + "(" + self.unit + ")" + ": "

        if self.t == int:
            self.value = get_number_in_range(desc_string, self.start, self.end)
        elif self.t == float:
            self.value = get_number(desc_string)
        elif self.t == str:
            self.value = input(desc_string)
        elif self.t == date:
            self.value = datetime.today().strftime("%d-%m-%Y")

        else:
            raise TypeError("Kategorian tyyppi ei ole tunnettu")


def get_number(text):
    """Asks user for input and checks that it is float"""
    user_input = input(text)
    # Check that input contains only digits and decimal separators
    while not user_input.replace(".", "", 1).isdigit():
        print("Anna numero")
        user_input = input(text)

    return user_input


def get_number_in_range(text, start, end):
    """Ask user for input and checks that it is integer between 'start' and 'end'"""
    user_input = input(text)

    # Check if start and end are None
    if start == None:
        start = float("-inf")
    if end == None:
        end = float("inf")

    while (
        user_input == ""
        or not user_input.isdigit()
        or int(user_input) < start
        or int(user_input) > end
    ):
        print("Anna numero")
        user_input = input(text)
    return user_input


class Cat(Enum):
    """Available categories"""

    DURATION = Category("Kesto", "mmm.ss", float, 0)
    HEART_RATE_AVG = Category("Syke keskiarvo", "numero", int, 0)
    HEART_RATE_MAX = Category("Syke maksimi", "numero", int, 0)
    DISTANCE = Category("Matka", "km", float, 0)
    SPEED = Category("Vauhti", "min/km", float, 0)
    STRENGTH_ESTIMATE = Category("Arvio omasta jaksamisesta", "numero", int, 1, 5)
    FEELING_ESTIMATE = Category("Olotila suorituksen jälkeen", "numero", int, 1, 5)
    DESCRIPTION = Category("Kuvaus", "teksti", str)
    SAVE = Category("Tarvitseeko tietoja muokata", "y/N", str)
    DATE = Category("Päivämäärä", "dd.mm.yyyy", date)
