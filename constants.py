import os

### General COMSOL data

# COMSOL files
MPH_FILES = [
    # 'input_files/SD-INLCN.mph',
    # 'input_files/DMND001.mph',
    # 'input_files/NACA4412.mph',
    'input_files/NACA4412PR1.mph',
    # 'input_files/BWRD.mph'
]

EXPORT_DICT = {
    1: "Continuous Phase Velocity",
    2: "Dispersed Phase Velocity",
    3: "Pressure",
    4: "Streamlines (Uc)",
    5: 'Separation Velocity (Ud - Uc), Arrow Surface',
    6: 'Dispersed Phase Volume Fraction',
    7: "Continuous Phase - Vorticity",
    8: 'Streamline Comparison',
    9: 'Velocity Difference',
    10: 'Volume Fraction and Difference Streamlines',
    11: 'Volume Fraction and Particle Streamlines'
}

EXPORT_PLOT_NODES = [EXPORT_DICT[1], EXPORT_DICT[2], EXPORT_DICT[3],
                     EXPORT_DICT[4], EXPORT_DICT[5], EXPORT_DICT[6]]

PNG_NAME_DICT = {
    'Continuous Phase Velocity': 'Uc',
    'Dispersed Phase Velocity': 'Ud',
    'Pressure': 'P',
    'Streamlines (Uc)': 'Uc, streamlines',
    'Separation Velocity (Ud - Uc), Arrow Surface': 'Ud-Uc, arrows',
    'Dispersed Phase Volume Fraction': 'phi',
}

EXPORT_OUTER_SOL_REQUIRED = {

}

EXPORT_DIRECTORY = "Exports/"

DISPLAY_NODE_TREE = False

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
PATH = os.environ["DYLD_LIBRARY_PATH"]

### Producing plots with prests

# Presets folder
if not os.path.exists("new_plot_presets/"):
    try:
        os.mkdir("new_plot_presets")
        if not os.path.exists("new_plot_presets/source_desc_values/"):
            try:
                os.mkdir("new_plot_presets/source_desc_values/")
            except Exception as e:
                print("Could not create the new plot presets subdirectory")
                raise e

    except Exception as e:
        print("Could not create new plot presets directory")
        raise e
new_presets_folder = "new_plot_presets/source_desc_values/"

# Preset ignore lists
PG_IGNORE_LIST = [
    'data',
    'looplevel',
    'outersolnum',
    'outertype',
    'solnum',
    'solrepresentation',
    'solutionparams',
    'title'
]

PLOT_IGNORE_LIST = [
    'actuallevels',
    'actuallevelslegend',
    'labels',
    'outersolnum',
    'outertype',
    'plotinfo',
    'rangeactualminmax',
    'rangecolormax',
    'rangecolormin',
    'rangedatamax',
    'rangedatamin',
    'rangeminpositive',
    'rangeunit',
    'rowindex',
    'solnum',
    'title',
    'unit',
]

### Difference contours data

# Array of all the files that need to be exported.
MINUENDS = ["dataset1.txt", "dataset1 copy.txt"]
SUBTRAHENDS = ["dataset2.txt"]