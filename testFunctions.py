from mphController import *
import os
from mphFunctions import *
from readPlotDesc import readAndExportPlotDescs
from newPlot import *

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

mph_files = ['input_files/BWRD.mph']

models, clients = mph_import_controller(mph_files, False)

readAndExportPlotDescs(models)
continuous_phase_velocity(models[0])
