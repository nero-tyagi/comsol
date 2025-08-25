import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.cm as cm
import os

def velocity_streamlines():
    # Load velocity data
    vel_data = np.loadtxt("velocity.txt", delimiter="\t")
    r, z, u_r, u_z = vel_data[:, 0], vel_data[:, 1], vel_data[:, 2], vel_data[:, 3]

    # Define a common grid for interpolation
    r_grid = np.linspace(min(r), max(r), 100)
    z_grid = np.linspace(min(z), max(z), 100)
    R, Z = np.meshgrid(r_grid, z_grid)

    # Interpolate velocity components onto grid
    U_r = griddata((r, z), u_r, (R, Z), method='cubic')
    U_z = griddata((r, z), u_z, (R, Z), method='cubic')

    # Compute velocity magnitude for coloring (optional)
    speed = np.sqrt(U_r**2 + U_z**2)

    # Plot the streamlines
    fig, ax = plt.subplots(figsize=(6, 6), dpi=600)
    plt.subplots_adjust(left=0.16, bottom=0.14)

    # Optional: velocity magnitude as background contour
    contourf = ax.contourf(R, Z, speed, 300, cmap="viridis")

    # Streamlines
    ax.streamplot(r_grid, z_grid, U_r.T, U_z.T, color='white', linewidth=0.8, density=1.5)

    # Colorbar
    cbar = plt.colorbar(contourf, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label("Velocity magnitude", fontsize=16)

    # Labels and title
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    ax.set_xlabel("r (cm)", fontsize=22)
    ax.set_ylabel("z (cm)", fontsize=22)
    ax.set_title("Velocity Streamlines", fontsize=22, pad=10)

    # Grid and styling
    ax.grid(True, alpha=0.3)
    ax.minorticks_on()
    ax.set_aspect('equal')  # For physical accuracy

    # Save figure
    out_dir = "Exports/velocity-streamlines/"
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(out_dir + "streamlines.png", dpi=600)
    fig.show()