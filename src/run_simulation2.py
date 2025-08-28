import os
import subprocess
import yaml
from eppy.modeleditor import IDF
from config import EPLUS_PATH, IDF_PATH, IDD_PATH, WEATHER_PATH, OUTPUT_DIR


def configure_simulation(idf, setpoint, wall_conductivity):
    """Modify IDF object with the given parameters."""
    for thermostat in idf.idfobjects["THERMOSTATSETPOINT:SINGLEHEATING"]:
        thermostat.Setpoint_Temperature = setpoint

    for mat in idf.idfobjects["MATERIAL"]:
        if "WALL" in mat.Name.upper():
            mat.Conductivity = wall_conductivity

    # Ensure outputs
    idf.newidfobject("OUTPUT:SQLITE", Option_Type="SimpleAndTabular")
    idf.newidfobject("OUTPUT:METER", Key_Name="Electricity:Facility", Reporting_Frequency="Annual")
    idf.newidfobject("OUTPUT:METER", Key_Name="NaturalGas:Facility", Reporting_Frequency="Annual")
    return idf


def run_simulation(modified_idf, output_folder):
    """Run EnergyPlus simulation with the given modified IDF."""
    os.makedirs(output_folder, exist_ok=True)
    cmd = [
        os.path.join(EPLUS_PATH, "energyplus"),
        "-w", WEATHER_PATH,
        "-d", output_folder,
        modified_idf
    ]
    print(f"Running simulation: {modified_idf}")
    subprocess.run(cmd, check=True)
    print(f"Simulation complete: {output_folder}")


def main(yaml_file):
    IDF.setiddname(IDD_PATH)

    # Load parameter grid
    with open(yaml_file, "r") as f:
        params = yaml.safe_load(f)

    for sim in params["simulations"]:
        scenario_name = sim["name"]
        output_folder = os.path.join(OUTPUT_DIR, scenario_name)
        modified_idf = os.path.join(output_folder, f"{scenario_name}.idf")

        idf = IDF(IDF_PATH, WEATHER_PATH)
        idf = configure_simulation(
            idf,
            setpoint=sim["thermostat_setpoint"],
            wall_conductivity=sim["wall_conductivity"]
        )

        # Save modified IDF
        os.makedirs(output_folder, exist_ok=True)
        idf.saveas(modified_idf)

        # Run simulation
        run_simulation(modified_idf, output_folder)


if __name__ == "__main__":
    main("simulation_params.yaml")
