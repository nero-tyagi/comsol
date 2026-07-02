import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import random

# minuend is the data file for what is being subtracted from and subtrahend is the data file for what is being
# subtracted. Both of these data files have to be arrays of filenames of the data files. If you only desire to subtract
# one dataset from another, input two single-element arrays. Otherwise, if you desire to first find the average of
# several contours, input multiple strings in the arrays. You can choose to average both datasets or either one.

# WARNING: Make sure that all the data files have the same length.

def generate_difference_contour(minuends_files, subtrahends_files):

    # Initializing matplotlib variables
    fig, ax = plt.subplots(figsize=(6, 6), dpi=600)
    plt.subplots_adjust(left=0.16)
    plt.subplots_adjust(bottom=0.14)

    # COMSOL returns data in a list of coordinates and their respective values. For example, if your x-coordinate has
    # 100 elements, the first 100 indices of the list will list all the x-values for the first y element. The second 100
    # values will be the x-values for the second y element, and so on. This is not a grid. In order to display a
    # contour, first the data needs to be represented in a grid where the x and y lengths of the grids represents the
    # physical elements of the model component.

    # Loading data files. The columns have to be delimited by "tab" and the header has to be removed.
    minuends = []
    subtrahends = []
    minuends_count = len(minuends_files)
    subtrahends_count = len(subtrahends_files)

    for i in range(0, minuends_count):
        minuends.append(np.loadtxt(minuends_files[i], delimiter="\t"))
    minuend_row_count = minuends[0].shape[0]

    for i in range(0, subtrahends_count):
        subtrahends.append(np.loadtxt(subtrahends_files[i], delimiter="\t"))
    subtrahend_row_count = subtrahends[0].shape[0]

    datasets_in_same_domain = False

    # Checking the minuends and the subtrahends to make sure they have the same dimensionality and are discretized in
    # the same way.
    if check_dimensionality(minuends, minuends_count, minuend_row_count):
        if check_dimensionality(subtrahends, subtrahends_count, subtrahend_row_count):
            datasets_in_same_domain = True

    if datasets_in_same_domain:
        minuend = np.zeros((minuend_row_count, 3))
        subtrahend = np.zeros((subtrahend_row_count, 3))
        # Populating minuend and subtrahend with both the dimensional values and the variable values, and then averaging the variable
        # values.
        for i in range(0, minuend_row_count):
            minuend[i][0] = minuends[0][i][0]
            minuend[i][1] = minuends[0][i][1]
            for j in range(minuends_count):
                minuend[:, 2] += minuends[j][:, 2]
            minuend[:, 2] /= minuends_count

        for i in range(0, subtrahend_row_count):
            subtrahend[i][0] = subtrahends[0][i][0]
            subtrahend[i][1] = subtrahends[0][i][1]
            for j in range(subtrahends_count):
                subtrahend[:, 2] += subtrahends[j][:, 2]
            subtrahend[:, 2] /= subtrahend_row_count

        # Extract columns

        r1, z1, minuendi = minuend[:, 0], minuend[:, 1], minuend[:, 2]  # Dataset 1: r, z, minuend
        r2, z2, subtrahendi = subtrahend[:, 0], subtrahend[:, 1], subtrahend[:, 2]  # Dataset 2: r, z, subtrahend

        # Define a common grid for interpolation
        r_grid = np.linspace(min(r1), max(r1), 5000)
        z_grid = np.linspace(min(z1), max(z1), 5000)
        R, Z = np.meshgrid(r_grid, z_grid)

        # Interpolate both datasets onto the common grid
        # minuend_grid = griddata((r1, z1), minuendi, (R, Z), method='cubic')
        minuend_grid = griddata((r1, z1), minuendi - subtrahendi, (R, Z))
        # subtrahend_grid = griddata((r2, z2), subtrahendi, (R, Z), method='cubic')

        # Compute the difference
        # difference = minuend_grid - subtrahend_grid
        difference = minuend_grid
    return R, Z, difference, fig, ax

def plot_contour(R, Z, var, ax, type=None, title=None, axes_titles=None, legend_pos=None):
    # Plot the difference as a contour plot
    contourf = ax.contourf(R, Z, var, 1000, cmap="seismic")  # Difference colormap

    # Colorbar
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    # cbar.set_label("$\v$ title")

    # Labels and title
    ax.set_xticks(range(-1, 25, 5))
    ax.set_yticks(range(-20, 30, 5))
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel("r (m)", fontsize=12)
    ax.set_ylabel("z (m)", fontsize=12)

    # Axes
    ax.set_xlim([-0.1, 0.16])
    ax.set_ylim([0.53, 0.73])

    # Grid
    ax.grid(True, alpha=0.3)
    ax.minorticks_on()
    ax.grid(True, which='minor', alpha=0.15)
    return ax

def check_dimensionality(array, length, rows):
    boolean = False
    if len(array) == 1:
        boolean = True
    else:
        for i in range(0, length):
            random_row = random.randint(0, rows)
            if array[0][random_row][0] == array[1][random_row][0]:
                if array[0][random_row][1] == array[1][random_row][1]:
                    boolean = True
                else:
                    boolean = False
            else:
                boolean = False
    return boolean