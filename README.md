
---

# Project Description

This project automates building energy modeling with EnergyPlus, modifies model parameters using eppy, runs simulations, and extracts energy consumption results from the SQL output using pandas.

## Main Steps

1. **IDF File Modification**  
   - Change building parameters (e\.g\. heating setpoint, wall conductivity).
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

1. Install dependencies:
   ```
   pip install eppy pandas
   ```
2. Make sure EnergyPlus is installed and example/weather files are available.
3. Run the main script:
   ```
   python src/test_energyplus.py
   ```

## Project Structure

- `src/test_energyplus.py` — main modeling and analysis script
- `test_building.idf` — modified EnergyPlus input file
- `simulation_output/eplusout.sql` — simulation SQL output file

## Results

The console displays the building's annual electricity and gas consumption (if gas is used in the model).

---

