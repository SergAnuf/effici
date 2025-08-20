import os
import subprocess
import sqlite3
import pandas as pd
from eppy.modeleditor import IDF

# === PATHS ===
EPLUS_PATH = "/usr/local/EnergyPlus-25-1-0"
IDF_PATH = os.path.join(EPLUS_PATH, "ExampleFiles", "1ZoneUncontrolled.idf")
IDD_PATH = os.path.join(EPLUS_PATH, "Energy+.idd")
WEATHER_PATH = os.path.join(EPLUS_PATH, "WeatherData", "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")

# Load EnergyPlus IDD
IDF.setiddname(IDD_PATH)

# Load baseline IDF
idf = IDF(IDF_PATH, WEATHER_PATH)

# === Modify the building ===
# Example: change heating setpoint to 22°C
for thermostat in idf.idfobjects["THERMOSTATSETPOINT:SINGLEHEATING"]:
    thermostat.Setpoint_Temperature = 22.0

# Example: change wall U-value by editing Material layer conductivity
for mat in idf.idfobjects["MATERIAL"]:
    if "WALL" in mat.Name.upper():
        print(f"Original wall conductivity for {mat.Name}: {mat.Conductivity}")
        mat.Conductivity = 0.5  # W/m-K (just for testing)

# Add Output:SQLite
idf.newidfobject(
    "OUTPUT:SQLITE",
    Option_Type="SimpleAndTabular"
)

# Add Output:Meter for electricity
idf.newidfobject(
    "OUTPUT:METER",
    Key_Name="Electricity:Facility",
    Reporting_Frequency="Annual"
)

# Add Output:Meter for natural gas
idf.newidfobject(
    "OUTPUT:METER",
    Key_Name="NaturalGas:Facility",
    Reporting_Frequency="Annual"
)

# Save new file
modified_idf = "test_building.idf"
idf.saveas(modified_idf)

# === Run EnergyPlus ===
output_dir = "simulation_output"
os.makedirs(output_dir, exist_ok=True)

cmd = [
    os.path.join(EPLUS_PATH, "energyplus"),
    "-w", WEATHER_PATH,
    "-d", output_dir,
    modified_idf
]

print("Running EnergyPlus...")
subprocess.run(cmd, check=True)
print("Simulation complete.")

# === Read results from SQL ===
sql_path = os.path.join(output_dir, "eplusout.sql")
con = sqlite3.connect(sql_path)
cur = con.cursor()

# Check if required tables exist
required_tables = {"ReportData", "ReportDataDictionary"}
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
existing_tables = {row[0] for row in cur.fetchall()}

if not required_tables.issubset(existing_tables):
    raise RuntimeError(f"Missing required tables: {required_tables - existing_tables}")

# Get annual total purchased electricity and gas (GJ)
query = """
SELECT rdd.Name, rd.Value
FROM ReportData rd
JOIN ReportDataDictionary rdd
ON rd.ReportDataDictionaryIndex = rdd.ReportDataDictionaryIndex
WHERE rdd.ReportingFrequency = 'Annual'
AND rdd.Name IN ('Electricity:Facility', 'NaturalGas:Facility')
"""
df = pd.read_sql_query(query, con)
con.close()

print("\nAnnual Energy Use (GJ):")
print(df)
