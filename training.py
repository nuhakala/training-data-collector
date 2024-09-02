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


from os.path import exists
import threading
# from Category import Cat
import Category
import utils


# ***** Start thread *****
weather_data = []
thr = threading.Thread(target=utils.get_weather_data, args=[weather_data], kwargs={})
thr.start()


# ***** Get training type *****
training_type = utils.read_training_type()

for i in training_type.categories:
    i.value.get_input()


# ***** Edit info if needed *****
for i in training_type.categories:
    if i == Category.Cat.SAVE:
        edit = i.value.value.lower() if i.value.value else "n"
        if edit == "y" or edit == "yes":
            utils.edit_values(training_type)


# ***** Write header line if file does not exist *****
save_file = utils.get_save_file_path()
file_exists = exists(save_file)
if not file_exists:
    with open(save_file, "x") as f:
        header_line = utils.get_cat_desc(Category.Cat.DATE)
        header_line += ",Tyyppi"
        for o in Category.Cat:
            if o != Category.Cat.SAVE:
                header_line += utils.get_cat_desc(o)

        header_line += utils.get_weather_url()[2]

        f.write(header_line + "\n")


# ***** Form the CSV row that is to be written *****
result = ""
# Add date
for i in training_type.categories:
    if i == Category.Cat.DATE:
        result += i.value.value if i.value.value else ""

# Add type
result += "," + training_type.shorthands[0]

# Add rest of the categories
for o in Category.Cat:
    if o != Category.Cat.SAVE and o != Category.Cat.DATE:
        if o in training_type.categories:
            result += "," + o.value.value if o.value.value else ""
        else:
            result += ","


# ***** Will wait till weather complete *****
if thr.is_alive():
    print("Odotetaan että sää on haettu...")
thr.join()

# ***** Add weather data to CSV row *****
if utils.track_weather:
    data = weather_data[0].split("|")
    # Condition can contain multiple value separated by commas, but commas will
    # break our csv-line, so replace them with ';'
    result += "," + data[0].replace(",", ";")  # condition
    # Number can be negative, so we need to add the sign with this check, because
    # isdigit does not recognize negative numbers
    result += "," + "".join(x for x in data[1] if x.isdigit() or x == "-")  # temperature
    result += "," + "".join(x for x in data[2] if x.isdigit() or x == "-")  # feels like
    result += "," + "".join(x for x in data[3] if x.isdigit() or x == "-")  # wind
    result += "," + "".join(x for x in data[4] if x.isdigit() or x == "-")  # humidity
else:
    res = ""
    for i in range(0, utils.get_weather_url()[1]):
        res += ","
    result += res


# ***** Write row to file *****
with open(save_file, "a") as myfile:
    myfile.write(result + "\n")
