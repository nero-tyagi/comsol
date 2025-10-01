import os

### General COMSOL data

# COMSOL files
MPH_FILES = [
    # 'input_files/SD-INLCN.mph',
    # 'input_files/DMND001.mph',
    'input_files/NACA4412.mph',
    # 'input_files/NACA4412PR1.mph',
    # 'input_files/BWRD.mph'
]

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