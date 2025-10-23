import os
from options.parsers.plotGroups import parse_plot_groups
from options.parsers.propertyIgnoreLists import parse_ignore_lists
from options.parsers.exportPresets import parse_export_presets

### COMSOL files

MPH_FILES = [
    'data/SDPR2.mph',
    # 'data/SDPR3.mph',
    # 'data/SDPR4.mph',
    # 'data/SDPR5.mph',
    # 'data/SDPR6.mph',
    # 'data/SDPR7.mph',
    # 'data/SDPR8.mph',
]

### Directories
# System
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
PATH = os.environ["DYLD_LIBRARY_PATH"]

# Data files
PRESETS_FOLDER = "presets_files/"
# WARNING: Do not change to just "exports" because of non-overwrite mode in batch exporting.
EXPORT_DIRECTORY = "data/exports/"

# Option files
JOBS_PATH = "options/jobs.xml"
PLOTGROUPS_PATH = "options/plotgroups.xml"
PROPERTY_IGNORE_LISTS_PATH = "options/property_ignore_lists.xml"

# Export presets
EXPORT_PRESETS_PATH = "presets_files/exports/exports.xml"
EXPORT_PRESET_1 = parse_export_presets(EXPORT_PRESETS_PATH)
EXPORT_PRESETS_1 = EXPORT_PRESET_1[0].props

### Options

# Plot options
PLOTGROUPS = parse_plot_groups(PLOTGROUPS_PATH)

# Preset ignore lists

IGNORE_LISTS = parse_ignore_lists(PROPERTY_IGNORE_LISTS_PATH)
PG_IGNORE_LIST = IGNORE_LISTS.lists[0].ignore
PLOT_IGNORE_LIST = IGNORE_LISTS.lists[1].ignore
EXPORT_IGNORE_LIST = IGNORE_LISTS.lists[2].ignore

# Export presets

# EXPORT_PRESET_1 = {
#     'aspectratio': float(1.0),
#     'background': 'color',
#     'colortheme': 'ClassicDark',
#     'fontsize': int(20),
#     'height': float(1000.0),
#     'heightmultiple': int(1),
#     'heightpx': int(1000),
#     'qualitylevel': int(100),
#     'resolution': int(96),
#     'showgrid': True,
#     'sourcetype': 'plotgroup',
#     'width': float(1000.0),
#     'widthpx': float(1000.0)
# }

### Difference contours data

# Array of all the files that need to be exported.
MINUENDS = ["dataset1.txt", "dataset1 copy.txt"]
SUBTRAHENDS = ["dataset2.txt"]

### Other constants

EXPORT_OUTER_SOL_REQUIRED = {

}

DISPLAY_NODE_TREE = False