# src/config.py
import os

# Path to the EnergyPlus installation directory
EPLUS_PATH = "/usr/local/EnergyPlus-25-1-0"

# Path to the example IDF (Input Data File) provided by EnergyPlus
IDF_PATH = os.path.join(EPLUS_PATH, "ExampleFiles", "1ZoneUncontrolled.idf")

# Path to the IDD (Input Data Dictionary) file required for working with IDF files
IDD_PATH = os.path.join(EPLUS_PATH, "Energy+.idd")

# Path to the weather data file used for simulations
WEATHER_PATH = os.path.join(EPLUS_PATH, "WeatherData", "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")

# Name of the modified IDF file that will be generated
MODIFIED_IDF = "test_building.idf"

# Directory where simulation output files will be stored
OUTPUT_DIR = "simulation_output"