# src/config.py
import os

EPLUS_PATH = "/usr/local/EnergyPlus-25-1-0"
IDF_PATH = os.path.join(EPLUS_PATH, "ExampleFiles", "1ZoneUncontrolled.idf")
IDD_PATH = os.path.join(EPLUS_PATH, "Energy+.idd")
WEATHER_PATH = os.path.join(EPLUS_PATH, "WeatherData", "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")
MODIFIED_IDF = "test_building.idf"
OUTPUT_DIR = "simulation_output"
