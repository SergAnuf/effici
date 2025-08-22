# src/run_simulation.py
import os
import subprocess
from eppy.modeleditor import IDF
from config import EPLUS_PATH, IDF_PATH, IDD_PATH, WEATHER_PATH, MODIFIED_IDF, OUTPUT_DIR


def configure_simulation():
    """
    Configures the EnergyPlus simulation by modifying the input IDF file.

    - Loads the IDD file required for working with IDF files.
    - Modifies the thermostat setpoint temperature to 22°C.
    - Updates the wall material conductivity to 0.5 W/m-K for testing purposes.
    - Adds necessary output objects to the IDF file:
        - `OUTPUT:SQLITE` for generating SQLite output.
        - `OUTPUT:METER` for annual electricity and natural gas consumption.
    - Saves the modified IDF file to the specified path.

    Raises:
        None
    """
    IDF.setiddname(IDD_PATH)  # Load the IDD file for EnergyPlus
    idf = IDF(IDF_PATH, WEATHER_PATH)  # Load the baseline IDF file and weather data

    # Modify thermostat setpoint temperature
    for thermostat in idf.idfobjects["THERMOSTATSETPOINT:SINGLEHEATING"]:
        thermostat.Setpoint_Temperature = 19.0

    # Update wall material conductivity
    for mat in idf.idfobjects["MATERIAL"]:
        if "WALL" in mat.Name.upper():
            print(f"Original wall conductivity for {mat.Name}: {mat.Conductivity}")
            mat.Conductivity = 0.5

    # Add output objects for SQLite and meter data
    idf.newidfobject("OUTPUT:SQLITE", Option_Type="SimpleAndTabular")
    idf.newidfobject("OUTPUT:METER", Key_Name="Electricity:Facility", Reporting_Frequency="Annual")
    idf.newidfobject("OUTPUT:METER", Key_Name="NaturalGas:Facility", Reporting_Frequency="Annual")

    # Save the modified IDF file
    idf.saveas(MODIFIED_IDF)


def run_simulation():
    """
    Runs the EnergyPlus simulation using the modified IDF file.

    - Creates the output directory if it does not exist.
    - Constructs the command to execute EnergyPlus with the following parameters:
        - Weather file path.
        - Output directory path.
        - Modified IDF file path.
    - Executes the EnergyPlus simulation using the subprocess module.
    - Prints messages indicating the start and completion of the simulation.

    Raises:
        subprocess.CalledProcessError: If the EnergyPlus simulation fails.
    """
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Construct the command to run EnergyPlus
    cmd = [
        os.path.join(EPLUS_PATH, "energyplus"),
        "-w", WEATHER_PATH,
        "-d", OUTPUT_DIR,
        MODIFIED_IDF
    ]

    # Run the EnergyPlus simulation
    print("Running EnergyPlus...")
    subprocess.run(cmd, check=True)
    print("Simulation complete.")


if __name__ == "__main__":
    """
    Main entry point of the script.

    - Configures the simulation by modifying the IDF file.
    - Runs the EnergyPlus simulation with the configured settings.
    """
    configure_simulation()
    run_simulation()
