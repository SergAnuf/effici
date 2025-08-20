# src/run_simulation.py
import os
import subprocess
from eppy.modeleditor import IDF
from config import EPLUS_PATH, IDF_PATH, IDD_PATH, WEATHER_PATH, MODIFIED_IDF, OUTPUT_DIR


def configure_simulation():
    IDF.setiddname(IDD_PATH)
    idf = IDF(IDF_PATH, WEATHER_PATH)
    for thermostat in idf.idfobjects["THERMOSTATSETPOINT:SINGLEHEATING"]:
        thermostat.Setpoint_Temperature = 22.0
    for mat in idf.idfobjects["MATERIAL"]:
        if "WALL" in mat.Name.upper():
            print(f"Original wall conductivity for {mat.Name}: {mat.Conductivity}")
            mat.Conductivity = 0.5
    idf.newidfobject("OUTPUT:SQLITE", Option_Type="SimpleAndTabular")
    idf.newidfobject("OUTPUT:METER", Key_Name="Electricity:Facility", Reporting_Frequency="Annual")
    idf.newidfobject("OUTPUT:METER", Key_Name="NaturalGas:Facility", Reporting_Frequency="Annual")
    idf.saveas(MODIFIED_IDF)


def run_simulation():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cmd = [
        os.path.join(EPLUS_PATH, "energyplus"),
        "-w", WEATHER_PATH,
        "-d", OUTPUT_DIR,
        MODIFIED_IDF
    ]
    print("Running EnergyPlus...")
    subprocess.run(cmd, check=True)
    print("Simulation complete.")


if __name__ == "__main__":
    configure_simulation()
    run_simulation()