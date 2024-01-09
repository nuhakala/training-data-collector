# Training diary

`training.py` is a python module for saving training data. It is a command line
tool, which asks the user for the data and then saves the data in csv format to
given file.

This module can also fetch weather data from `wttr.in` if wanted. Weather
data is fetched asynchronously when filling up the data. Fetching weather data
can be also disabled.

This module does not have any dependencies, it uses python threads for
asynchronous execution and `wttr.in` is free website for getting weather data.
It does not even require API key like OpenWeatherMap API.

## Usage

You can configure it via env-variables.

``` bash
export TRAINIG_FILE=~/treenit.csv
export TRAINING_WEATHER=false
export TRAINING_LOCATION=aachen
```

The data file is `~/treenit.csv` by default, or if an env variable `TRAINIG_FILE`
exists, it sets the training data location.

This module can also fetch weather data from `wttr.in` if wanted. If you want to
disable weather tracking, then set env variable `TRAINING_WEATHER=false`. Weather
data is fetched asynchronously when filling up the data.

By default there is no training location, and `wttr.in` gets the weather by
IP-address. However, you can set the location (city) with `TRAINING_LOCATION`
env variable if you want.

