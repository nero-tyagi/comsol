import os

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
PATH = os.environ["DYLD_LIBRARY_PATH"]
PRESETS_FOLDER = "presets_files/"
EXPORT_DIRECTORY = "input_files/exports/"

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

## Dictionaries

# COMSOL files
MPH_FILES = [
    # 'input_files/SDPR2.mph',
    # 'input_files/SDPR3-1.mph',
    # 'input_files/SDPR3-2.mph',
    # 'input_files/SDPR3-3.mph',
    'input_files/SDPR3-4.mph',
    # 'input_files/SDPR3-5.mph',
    # 'input_files/SDPR3-6.mph',
    # 'input_files/SDPR4.mph',
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
}

PNG_NAME_DICT = {
    'Continuous Phase Velocity': 'Uc',
    'Dispersed Phase Velocity': 'Ud',
    'Pressure': 'P',
    'Streamlines (Uc)': 'Uc, streamlines',
    'Separation Velocity (Ud - Uc), Arrow Surface': 'Ud-Uc, arrows',
    'Dispersed Phase Volume Fraction': 'phi',
}

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
    'unit'
]

EXPORT_IGNORE_LIST = [
    'epsfilename',
    'heightexact',
    'jpegfilename',
    'lastwrittenfile'
    'sizedesc',
    'tifffilename'
]

EXPORT_PRESET_1M = {
    'aspectratio': float(1.0),
    'background': 'color',
    'colortheme': 'ClassicDark',
    'fontsize': int(20),
    'height': float(1000.0),
    'heightmultiple': int(1),
    'heightpx': int(1000),
    'qualitylevel': int(100),
    'resolution': int(96),
    'showgrid': True,
    'sourcetype': 'plotgroup',
    'width': float(1000.0),
    'widthpx': float(1000.0)
}

EXPORT_PRESET_1S = {
    'aspectratio': float(1.0),
    'background': 'color',
    'colortheme': 'ClassicDark',
    'fontsize': int(10),
    'height': float(500.0),
    'heightmultiple': int(1),
    'heightpx': int(500),
    'qualitylevel': int(100),
    'resolution': int(96),
    'showgrid': True,
    'sourcetype': 'plotgroup',
    'width': float(500.0),
    'widthpx': float(500.0)
}

EXPORT_PRESET_1L = {
    'aspectratio': float(1.0),
    'background': 'color',
    'colortheme': 'ClassicDark',
    'fontsize': int(40),
    'height': float(2000.0),
    'heightmultiple': int(1),
    'heightpx': int(2000),
    'qualitylevel': int(100),
    'resolution': int(96),
    'showgrid': True,
    'sourcetype': 'plotgroup',
    'width': float(2000.0),
    'widthpx': float(2000.0)
}

EXPORT_PRESET_1XL = {
    'aspectratio': float(1.0),
    'background': 'color',
    'colortheme': 'ClassicDark',
    'fontsize': int(80),
    'height': float(4000.0),
    'heightmultiple': int(1),
    'heightpx': int(4000),
    'qualitylevel': int(100),
    'resolution': int(96),
    'showgrid': True,
    'sourcetype': 'plotgroup',
    'width': float(4000.0),
    'widthpx': float(4000.0)
}

### Difference contours data

# Array of all the files that need to be exported.
MINUENDS = ["dataset1.txt", "dataset1 copy.txt"]
SUBTRAHENDS = ["dataset2.txt"]

### Other constants

EXPORT_PLOT_NODES = [EXPORT_DICT[1], EXPORT_DICT[2], EXPORT_DICT[3],
                     EXPORT_DICT[4], EXPORT_DICT[5], EXPORT_DICT[6]]

EXPORT_OUTER_SOL_REQUIRED = {

}

DISPLAY_NODE_TREE = False