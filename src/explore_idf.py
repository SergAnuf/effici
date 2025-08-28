from config import EPLUS_PATH, IDF_PATH, IDD_PATH, WEATHER_PATH, MODIFIED_IDF, OUTPUT_DIR
from eppy.modeleditor import IDF

IDF.setiddname(IDD_PATH)  # Load the IDD file for EnergyPlus
idf = IDF(IDF_PATH, WEATHER_PATH)

# Name of the material to inspect
material_name = "R13LAYER"

# Find the material in the IDF
materials = idf.idfobjects["MATERIAL:NOMASS"]
material = None
for mat in materials:
    if mat.Name.upper() == material_name.upper():
        material = mat
        break

# Print material properties
if material:
    print(dir(material))
    # print(f"Material: {material.Name}")
    # print(f"  Roughness: {material.Roughness}")
    # print(f"  Thickness: {material.Thickness} m")
    # print(f"  Conductivity: {material.Conductivity} W/m-K")
    # print(f"  Density: {material.Density} kg/m³")
    # print(f"  Specific Heat: {material.Specific_Heat} J/kg-K")
    # print(f"  Thermal Absorptance: {material.Thermal_Absorptance}")
    # print(f"  Solar Absorptance: {material.Solar_Absorptance}")
    # print(f"  Visible Absorptance: {material.Visible_Absorptance}")
    print(material.Thermal_Resistance)
else:
    print(f"Material '{material_name}' not found in the IDF.")