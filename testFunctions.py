from mphController import *
import os
from mphFunctions import *
import mph

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

mph_files = ['input_files/SD-INLCN.mph']

models, clients = mph_import_controller(mph_files, True)

plot_node = models[0]/'plots'/'Continuous Phase - Velocity'
sub_plot_node = models[0]/'plots'/'Continuous Phase - Velocity'/'Surface 1'

get_node_properties(models[0], plot_node, "plot")
get_node_properties(models[0], sub_plot_node, "surface_subplot")
