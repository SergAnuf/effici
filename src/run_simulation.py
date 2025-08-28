# src/run_simulation.py
import os
import yaml
import subprocess
from eppy.modeleditor import IDF
from config import EPLUS_PATH, IDF_PATH, IDD_PATH, WEATHER_PATH, MODIFIED_IDF, OUTPUT_DIR, PARAMETERS_DIR


def configure_simulation(idf, thermal_resistance=2.321, wind_direction=128.0):
    """
    Configures the EnergyPlus simulation by modifying the input IDF file.

    Parameters:
        idf (IDF): The IDF object to be modified.
        thermal_resistance (float): The thermal resistance value to set for the specified material.
        wind_direction (float): The wind direction value to set in the design day sizing period.

    Returns:
        IDF: The modified IDF object.
    """
    # Modify material properties
    material_name = "R13LAYER"
    for mat in idf.idfobjects["MATERIAL:NOMASS"]:
        if mat.Name.upper() == material_name.upper():
            mat.Thermal_Resistance = thermal_resistance

    # Change wind direction in SizingPeriod:DesignDay
    for spdd in idf.idfobjects["SIZINGPERIOD:DESIGNDAY"]:
        spdd.Wind_Direction = wind_direction

    # Add output objects for SQLite and meter data
    idf.newidfobject("OUTPUT:SQLITE", Option_Type="SimpleAndTabular")
    idf.newidfobject("OUTPUT:METER", Key_Name="Electricity:Facility", Reporting_Frequency="Annual")
    idf.newidfobject("OUTPUT:METER", Key_Name="NaturalGas:Facility", Reporting_Frequency="Annual")

    # Save the modified IDF file
    return idf


def run_simulation(modified_idf, output_folder):
    """
    Runs the EnergyPlus simulation using the specified modified IDF file.

    Parameters:
        modified_idf (str): Path to the modified IDF file.
        output_folder (str): Path to the folder where simulation results will be stored.

    Raises:
        subprocess.CalledProcessError: If the EnergyPlus simulation fails.
    """
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Construct the command to run EnergyPlus
    cmd = [
        os.path.join(EPLUS_PATH, "energyplus"),
        "-w", WEATHER_PATH,
        "-d", output_folder,
        modified_idf
    ]

    # Run the EnergyPlus simulation
    print(f"Running simulation: {modified_idf}")
    subprocess.run(cmd, check=True)
    print(f"Simulation complete: {output_folder}")


def main(yaml_file):
    """
    Main function to configure and run EnergyPlus simulations based on a parameter grid.

    Parameters:
        yaml_file (str): Path to the YAML file containing simulation parameters.

    Workflow:
        1. Loads the parameter grid from the YAML file.
        2. Iterates over each simulation scenario in the parameter grid.
        3. Configures the IDF file for each scenario.
        4. Saves the modified IDF file to the output folder.
        5. Runs the EnergyPlus simulation for each scenario.
    """
    # Set the IDD file for EnergyPlus
    IDF.setiddname(IDD_PATH)

    # Load parameter grid
    with open(yaml_file, "r") as f:
        params = yaml.safe_load(f)

    # Iterate over simulation scenarios
    for sim in params["simulations"]:
        scenario_name = sim["name"]
        output_folder = os.path.join(OUTPUT_DIR, scenario_name)
        modified_idf = os.path.join(output_folder, f"{scenario_name}.idf")

        # Load and configure the IDF file
        idf = IDF(IDF_PATH, WEATHER_PATH)
        idf = configure_simulation(
            idf,
            thermal_resistance=sim["Thermal_Resistance"],
            wind_direction=sim["Wind_Direction"]
        )

        # Save modified IDF
        os.makedirs(output_folder, exist_ok=True)
        idf.saveas(modified_idf)

        # Run simulation
        run_simulation(modified_idf, output_folder)


if __name__ == "__main__":
    """
    Entry point of the script.

    - Loads the parameter grid from the specified YAML file.
    - Configures and runs EnergyPlus simulations for each scenario in the parameter grid.
    """
    main(PARAMETERS_DIR)