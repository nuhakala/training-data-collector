"""
This module contains some utilities for:
    - Fetching weather data
    - Resolving save file path
    - Reading user input related to categories
    - Editing user input values
"""

import os
import subprocess
import tempfile
import requests
from TrainingTypes import TRAIN_TYPES, TrainingType


def get_save_file_path():
    return os.path.expanduser(
        os.path.expandvars(os.environ.get("TRAINING_FILE", "$HOME/treenit.csv"))
    )


def get_weather_url():
    location = os.environ.get("TRAINING_LOCATION", "")
    # Needs to correspond to format separator to generate correct csv-line
    # in case of error in getting weather data
    # Separator is '|' but there is five sections.
    num_weather_sections = 5
    return (
        "https://www.wttr.in/" + location + "?format=%C+|+%t+|+%f+|+%w+|+%h",
        num_weather_sections,
        ",Pilvisyys,Lämpötila,Lämpötila tuntuu,Tuulen nopeus (km/h),Ilmankosteus (%)",
    )


def track_weather():
    return os.environ.get("TRAINING_WEATHER", "true").lower() == "true"


def get_weather_data(res):
    """Function for making http-request for fetching weather data"""
    if track_weather:
        url = get_weather_url()
        try:
            # For whatever reason using long url gives 200 and basic one gives 503
            check_status = requests.get("https://www.wttr.in")
            r = requests.get(url[0], timeout=10)
            if check_status.status_code == 200:
                res.append(r.text)
            else:
                res.append("|")
                for _ in range(0, url[1]):
                    res[0] += "|"
        except requests.exceptions.RequestException:
            print("\n\nError fetching weather data, omitting this time.\n")
            # Populate weather_data with correct number of elements
            res.append("|")
            for _ in range(0, url[1]):
                res[0] += "|"


def read_training_type() -> TrainingType:
    print_msg = ""
    print_msg += "Valitse treenityyppi: "

    for i in TRAIN_TYPES:
        print_msg += i.name + "("
        print_msg += "'" + i.shorthands[0] + "'"
        for e in i.shorthands[1:]:
            print_msg += ", '" + e + "'"
        print_msg += "), "

    print_msg = print_msg[0:-2]
    print_msg += ": "
    training_type_input = input(print_msg)

    # Find correct traiting type
    for i in TRAIN_TYPES:
        if training_type_input in i.shorthands:
            return i

    # If correct type not found, recursively ask again
    print("Anna oikea tyyppi.")
    return read_training_type()


def edit_values(training_type):
    # Form value-array which we print to file
    msg_array = []
    for i in training_type.categories:
        msg_array.append(get_cat_desc(i) + ": " + i.value.value)

    # Open temp file
    f = tempfile.NamedTemporaryFile(suffix=".tmp")
    initial_message = "# Jokainen avain-arvo pari omalle riville.\n"
    initial_message += "# Älä laita väärää arvoa, koska niitä ei tarkisteta.\n"
    initial_message += "# Älä muokkaa kaksoispisteen vasenta puolta.\n"
    initial_message += "# Älä käytä pilkkuja, koska ne sotkee CSV tiedoston.\n\n"
    initial_message += "\n".join(msg_array)
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
        for o in training_type.categories:
            if get_cat_desc(o) == pair[0]:
                o.value.value = pair[1].strip()
    f.close()


def get_cat_desc(cat):
    return cat.value.description.strip() + " (" + cat.value.unit.strip() + ")"
