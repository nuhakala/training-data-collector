"""
This module is a utility for saving training data. It is a command line tool,
which asks the user for the data and then saves the data in csv format to given
file.

The file is either ~/treenit.csv or if an env variable `TRAINING_FILE` exists, it
is used.

This module can also fetch weather data from `wttr.in` if wanted. If you want to
disable weather tracking, then set env variable `TRAINING_WEATHER=false`. Weather
data is fetched asynchronously when filling up the data.

By default there is no training location, and `wttr.in` gets the weather by
IP-address. However, you can set the location (city) wwith `TRAINING_LOCATION`
env variable if you want.
"""


import os
import subprocess
import tempfile
from enum import Enum
from os.path import exists
from datetime import datetime
import requests
import threading


TRAIN_TYPES = ["j", "h", "y", "a"]
ESTIMATE_VALUES = [1, 2, 3, 4, 5]
save_file = os.path.expanduser(
    os.path.expandvars(os.environ.get("TRAINING_FILE", "~/treenit.csv"))
)
location = os.environ.get("TRAINING_LOCATION", "")
url = "https://www.wttr.in/" + location + "?format=%C+|+%t+|+%f+|+%w+|+%h"

# Needs to correspond to format separator to generate correct csv-line
# in case of error in getting weather data
# Separator is '|' and there is four of them in format.
num_weather_sections = 4
track_weather = os.environ.get("TRAINING_WEATHER", "true").lower() == "true"
# List is mutable, modifications apply outside
weather_data = []
error = False


# Function for getting weather data asynchronously
def get_weather_data():
    if track_weather:
        try:
            r = requests.get(url, timeout=10)
            weather_data.append(r.text)
        except requests.exceptions.RequestException:
            print("\n\nError fetching weather data, omitting this time.\n")
            # Populate weather_data with correct number of elements
            weather_data.append("")
            for _ in range(0, 5):
                weather_data[0] += "|"


# Start thread
thr = threading.Thread(target=get_weather_data, args=[], kwargs={})
thr.start()


class Desc(Enum):
    TYPE = "Tyyppi (Juoksu | Hiihto | sali/Ylävartalo | sali/jAlat)"
    DURATION = "Kesto (mmm.ss)"
    HEART_RATE_AVG = "Syke keskiarvo"
    HEART_RATE_MAX = "Syke maksimi"
    DISTANCE = "Matka (km)"
    SPEED = "Keskivauhti (min/km)"
    STRENGTH_ESTIMATE = "Arvio omasta jaksamisesta (1-5)"
    FEELING_ESTIMATE = "Olotila suorituksen jälkeen (1-5)"
    DESCRIPTION = "Kuvaus"
    SAVE = "Muokataanko? (N/y)"
    DATE = "Päivämäärä"


# Few helper functions
def get_number(text):
    user_input = input(text)
    if user_input == "":
        return ""
    # Replace decimal separator with 1
    while not user_input.replace(".", "", 1).isdigit():
        print("Anna numero")
        user_input = input(text)

    return user_input


def get_number_in_range(text):
    user_input = input(text)
    if user_input == "":
        return ""
    # Replace decimal separator with 1
    while (
        user_input == ""
        or not user_input.isdigit()
        or int(user_input) not in ESTIMATE_VALUES
    ):
        print("Anna numero")
        user_input = input(text)

    return user_input


# Read values
values = {}
values[Desc.TYPE] = input(Desc.TYPE.value + ": ")
while values[Desc.TYPE].lower()[0:1] not in TRAIN_TYPES:
    print("Väärä tyyppi")
    values[Desc.TYPE] = input(Desc.TYPE.value + ": ")


values[Desc.DURATION] = get_number(Desc.DURATION.value + ": ")
values[Desc.DISTANCE] = get_number(Desc.DISTANCE.value + ": ")
values[Desc.HEART_RATE_AVG] = get_number(Desc.HEART_RATE_AVG.value + ": ")
values[Desc.HEART_RATE_MAX] = input(Desc.HEART_RATE_MAX.value + ": ")
values[Desc.SPEED] = get_number(Desc.SPEED.value + ": ")
values[Desc.STRENGTH_ESTIMATE] = get_number_in_range(
    Desc.STRENGTH_ESTIMATE.value + ": "
)
values[Desc.FEELING_ESTIMATE] = get_number_in_range(Desc.FEELING_ESTIMATE.value + ": ")
values[Desc.DESCRIPTION] = input(Desc.DESCRIPTION.value + ": ")
values[Desc.SAVE] = input(Desc.SAVE.value + ": ")
values[Desc.DATE] = datetime.today().strftime("%d-%m-%Y")
while values[Desc.SAVE].lower()[0:1] not in ["n", "y", ""]:
    values[Desc.SAVE] = input(Desc.SAVE.value)


def get_message_array():
    res = []
    for o in Desc:
        if o != Desc.SAVE:
            res.append(o.value + ": " + values[o])
    return res


if values[Desc.SAVE].lower() == "y" or values[Desc.SAVE].lower() == "yes":
    # Open temp file
    f = tempfile.NamedTemporaryFile(suffix=".tmp")
    initial_message = "# Jokainen avain-arvo pari omalle riville.\n"
    initial_message += "# Älä laita väärää arvoa, koska niitä ei tarkisteta.\n"
    initial_message += "# Älä käytä pilkkuja, koska ne sotkee CSV tiedoston.\n\n"
    initial_message += "\n".join(get_message_array())
    f.write(initial_message.encode("utf-8"))
    f.flush()

    # open editor
    editor = os.environ.get("EDITOR", "nano")
    subprocess.call([editor, f.name])

    # Read the file
    f.seek(0)
    result = f.read().decode("utf-8")
    lines = result.strip().split("\n")

    # Lambda: filter comments
    for line in filter(lambda n: n[0:1] != "#", lines):
        pair = line.split(":")
        for o in Desc:
            if o.value == pair[0]:
                values[o] = pair[1].strip()
    f.close()


file_exists = exists(save_file)
if not file_exists:
    with open(save_file, "x") as f:
        header_line = "Päivämäärä (dd-mm-yyyy)"
        for o in Desc:
            if o != Desc.SAVE:
                header_line += "," + o.value.strip()

        if track_weather:
            header_line += ",Pilvisyys,Lämpötila,Lämpötila tuntuu,Tuulen nopeus (km/h),Ilmankosteus (%)"

        f.write(header_line + "\n")


# Write result, no loop to ensure that order is always the same

result = values[Desc.DATE]
for o in Desc:
    if o != Desc.SAVE and o != Desc.DATE:
        result += "," + values[o]
# result = date + "," + values[Desc.TYPE]
# result += "," + values[Desc.DURATION]
# result += "," + values[Desc.HEART_RATE_MAX]
# result += "," + values[Desc.DISTANCE]
# result += "," + values[Desc.SPEED]
# result += "," + values[Desc.STRENGTH_ESTIMATE]
# result += "," + values[Desc.FEELING_ESTIMATE]
# result += "," + values[Desc.DESCRIPTION]


if thr.is_alive():
    print("Odotetaan että sää on haettu...")

thr.join()  # Will wait till weather complete

if track_weather:
    data = weather_data[0].split("|")
    # Condition can contain multiple value separated by commas, but commas will
    # break our csv-line, so replace them with ';'
    result += "," + data[0].replace(",", ";")  # condition
    # Number can be negative, so we need to add the sign with this check, because
    # isdigit does not recognize negative numbers
    result += "," + "".join(
        x for x in data[1] if x.isdigit() or x == "-"
    )  # temperature
    result += "," + "".join(x for x in data[2] if x.isdigit() or x == "-")  # feels like
    result += "," + "".join(x for x in data[3] if x.isdigit() or x == "-")  # wind
    result += "," + "".join(x for x in data[4] if x.isdigit() or x == "-")  # humidity


with open(save_file, "a") as myfile:
    myfile.write(result + "\n")
