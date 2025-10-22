import os

### Important directories

os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
PATH = os.environ["DYLD_LIBRARY_PATH"]
PRESETS_FOLDER = "presets_files/"
# WARNING: Do not change to just "exports" because of non-overwrite mode in batch exporting.
EXPORT_DIRECTORY = "input_files/exports/"
JOBS_PATH = "input_files/jobs.xml"

### Presets folder

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

### Preset ignore lists

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

### Export presets

EXPORT_PRESET_1 = {
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

### Difference contours data

# Array of all the files that need to be exported.
MINUENDS = ["dataset1.txt", "dataset1 copy.txt"]
SUBTRAHENDS = ["dataset2.txt"]

### Other constants

EXPORT_OUTER_SOL_REQUIRED = {

}

DISPLAY_NODE_TREE = False