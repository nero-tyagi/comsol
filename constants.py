import os

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

# Array of all the files that need to be exported.
minuends = ["dataset1.txt", "dataset1 copy.txt"]
subtrahends = ["dataset2.txt"]

# COMSOL files
mph_files = [
    'input_files/SD-INLCN.mph',
    'input_files/DMND001.mph',
    'input_files/NACA4412.mph',
    'input_files/NACA4412PR1.mph',
    # 'input_files/BWRD.mph'
]