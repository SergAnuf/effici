---

# Project Description

This project automates building energy modeling with EnergyPlus: it modifies model parameters using eppy, runs simulations, and extracts energy consumption results from the SQL output using pandas.

## Main Steps

1. **IDF File Modification**
   - Change building parameters (e.g. heating setpoint, wall conductivity).
   - Add `Output:SQLite` and `Output:Meter` objects for required reports.

2. **Run EnergyPlus Simulation**
   - Use the modified IDF and weather data.

3. **Result Analysis**
   - Read the SQL output and extract annual electricity and gas consumption.

## Requirements

- Python 3.10+
- EnergyPlus 25.1.0
- eppy
- pandas
- sqlite3

## Quick Start

1. Install dependencies:2. Make sure EnergyPlus is installed and example/weather files are available.
3. Run simulation preparation and execution:4. Analyze results:## Project Structure

- `src/run_simulation.py` — prepares and runs the EnergyPlus simulation
- `src/analyze_results.py` — analyzes results from the SQL output
- `src/config.py` — project paths and parameters
- `src/utils.py` — helper functions
- `src/simulation_output/` — EnergyPlus output files
- `src/test_building.idf` — modified EnergyPlus input file

## Results

The console displays the building's annual electricity and gas consumption (if gas is used in the model).

---## Project Structure

- `src/run_simulation.py` — prepares and runs the EnergyPlus simulation
- `src/analyze_results.py` — analyzes results from the SQL output
- `src/config.py` — project paths and parameters
- `src/utils.py` — helper functions
- `src/simulation_output/` — EnergyPlus output files
- `src/test_building.idf` — modified EnergyPlus input file

## Results

The console displays the building's annual electricity and gas consumption (if gas is used in the model).

