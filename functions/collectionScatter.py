import plotly.express as px
import pandas as pd
import numpy as np
import os
from constants import EXPORT_DIRECTORY, CM_FILE

filename_prefix = 'Cm_dot_scatter'

def create_mass_flow_scatter(filename_prefix = filename_prefix):
    directory = EXPORT_DIRECTORY
    # scatter_points.sort(key=lambda x: x['theta'])
    df_dict = {
        'Name': 'Model name',
        'Ws': 'Width-height ratio (w:h)',
        'Hs': 'Gap-height ratio (H:h)',
        'theta': 'Coupon angle',
        'aoa': 'Angle of attack',
        'theta_c': 'Cone angle',
        'Cm_dot': 'DP mass flow rate ratio (outlet:mean)'
    }
    df = pd.read_excel(CM_FILE, names=list(df_dict.keys()))
    print(df)

    x_var = 'Hs'
    color_var = 'aoa'
    bubble_var = 'Ws'
    fig = px.scatter(df, x=x_var, y='Cm_dot',
                     color=color_var, size=bubble_var)

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text=x_var
            )
        ),
        yaxis=dict(
            title=dict(
                text='Outlet/mean dispersed phase mass flow rate'
            )
        ),
        font=dict(size=16),
    )
    print("Writing scatter plot files...")
    if not os.path.isdir(EXPORT_DIRECTORY):
        os.mkdir(EXPORT_DIRECTORY)
    if not os.path.isdir(EXPORT_DIRECTORY + "scatter/"):
        try:
            os.mkdir(EXPORT_DIRECTORY + "scatter/")
        except Exception:
            print("Failed to create directory")
    fig.write_html(EXPORT_DIRECTORY + 'scatter/' + x_var + '.html')
    fig.write_image(directory + 'scatter/' + x_var + '.png', format='png', scale=1, width=1000, height=1000)
    print("Scatter plot files written.")
    # fig.show()

def calc_mdot():
    column_names = ['r', 'Ws', 'Hs', 'theta', 'phid', 'udz']
    df = pd.read_table("data/outlet.txt", sep='\t', skiprows=9, header=None,
                       names=column_names, dtype=float)

    mdot = np.zeros(len(df['r']))

    for i in range(2, len(df['r'])):
        mdot[i] = (2 * np.pi *
                   ((df['r'].iloc[i])) / 100 *
                   ((df['r'].iloc[i]) - (df['r'].iloc[i - 1])) / 100 *
                   (-1 * df['udz'].iloc[i]) *
                   1200 *
                   df['phid'].iloc[i] / 1E6)

    total_flow_rate = sum(mdot)
    return total_flow_rate