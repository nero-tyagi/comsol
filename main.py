import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from contourFunctions import generate_difference_contour, plot_contour
from particle_collection_scatter import create_point_for_scatter
from mphController import mph_import_controller
from constants import *

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

# Array of all the files that need to be exported.
minuends = ["dataset1.txt", "dataset1 copy.txt"]
subtrahends = ["dataset2.txt"]

mph_files = [
    # 'input_files/SD-INLCN.mph',
    'input_files/BWRD-small_data.mph'
    # 'input_files/BWRD.mph'
]

if __name__ == '__main__':
    # arr = [0, 1, 2, 3, 4, 5]
    # total = [0, 0, 0, 0, 0, 0]
    # for i in arr:
    #     column_names = ['r', 'udz', 'phi']
    #     df = pd.read_table('ef-' + str(i) + ', phi-line.txt', sep='\t', names=column_names, dtype=float)
    #     sum = 0
    #     average_phi = 0
    #     for j in range(1, 100):
    #         average_phi += df['phi'][j]
    #     average_phi /= 100
    #     for j in range(1, len(df['r'])):
    #         sum += (df['r'][j] - df['r'][j - 1]) * (df['phi'][j]-average_phi)
    #     print(sum)

    # R, Z, difference, fig, ax = generate_difference_contour(minuends, subtrahends)
    # ax = plot_contour(R, Z, difference, ax)
    # # Save figure
    # directory= "Test/Exports/"
    # os.makedirs(directory, exist_ok=True)
    # fig.savefig(directory + "test_contour.png", dpi=600)
    # fig.show()

    #ax.set_title(r"$\phi_{St =" + str(Sts[-1]) + "} - \phi_{St = " + str(Sts[0]) + "}$", fontsize=22, pad=10)