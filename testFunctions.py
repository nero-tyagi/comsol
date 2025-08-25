from mphController import *
import os
from getFunctions import *

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

mph_files = ['SD-INLCN.mph']

mph_import_controller(mph_files, True)