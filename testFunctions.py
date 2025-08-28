from mphController import *
import os
from mphFunctions import *
from generatePlotPresets import readAndExportPlotDescs
from newPlot import *

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

mph_files = [
    # 'input_files/BWRD.mph',
    'input_files/BWRD-small_data.mph',
    'input_files/SD-INLCN.mph'
]

models, clients = mph_import_controller(mph_files, False)

# readAndExportPlotDescs(models[0])
plots = [1, 2, 3, 4, 5, 6]
for model in models:
    for plot in plots:
        generate_pg(model, pg_name=preset_plots.get(plot))

