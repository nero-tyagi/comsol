# import plotly.express as px
import pandas as pd
import numpy as np
import os
from scipy import integrate

filename_prefix = 'design_variable_comparison'
show_plots = True

def create_point_for_scatter(filename, column_names=None):
    if column_names is None:
        column_names = ['r', 'udz', 'phi']
    rho_d = 1200
    r_i = 0.15
    df = pd.read_table(filename, sep='\s+', names=column_names, dtype=float)

    mass_rate = 0
    for i in range(1, len(df[str(column_names[0])]), 1):
        mass_rate += (2 * np.pi * r_i *
                      (df['r'][i] - df['r'][i - 1]) *
                      df['udz'][i] * (df['r'][i] - 0.85) *
                      rho_d * df['phi'][i] / 1E6)
        # mass_rate += (2 * np.pi * df[str(column_names[0])][i - 1] *
        #               (df[str(column_names[0])][i] - df[str(column_names[0])][i - 1]) *
        #               df[str(column_names[3])][i - 1] * rho_c * df[str(column_names[2])][i - 1] / 1E6)
        print(rho_d * df['phi'][i] / 1E6)
    return mass_rate


def populate_scatter_data(variables, directory, filename):
    scatter_points = []

    # Reading data files to create points for particle collection scatter:
    i = 0
    for x in os.walk(directory):
        try:
            if i != 0: # Because the first index is the directory itself
                scatter_points.append(create_point_for_scatter(x[0] + '/' + filename,
                                                               list(variables.keys())))
            i += 1
        except Exception as e:
            print("Could not create scatter data for " + x[0])
            print(e)
    # for value in scatter_f
    print()
    print(str(len(scatter_points)) + " points created.")

    return scatter_points

# def create_mass_flow_scatter(scatter_points, variables, directory = "", filename_prefix = ""):
#     scatter_points.sort(key=lambda x: x['theta'])
#     df_dict = {
#         'ar_Hh': 'Gap-height ratio (H:h)',
#         'ar_wh': 'Width-height ratio (w:h)',
#         'mass_rate': 'Mass flow',
#         'theta': 'Angle',
#     }
#
#     df = pd.DataFrame({df_dict.get('ar_Hh'): [(point.get('ar_Hh')) for point in scatter_points],
#                         df_dict.get('ar_wh'): [(point.get('ar_wh')) for point in scatter_points],
#                         df_dict.get('theta'): [str(point.get('theta')) for point in scatter_points],
#                         df_dict.get('mass_rate'): [point.get('mass_rate') for point in scatter_points]})
#
#     x_var = df_dict.get('ar_wh')
#     color_var = df_dict.get('theta')
#     bubble_var = df_dict.get('ar_Hh')
#     fig = px.scatter(df, x=x_var, y='Mass flow',
#                      color=color_var, size=bubble_var)
#     # fig = px.scatter(df, x=x_var, y='Mass flow',
#     #                  color=color_var)
#
#     fig.update_layout(
#         xaxis=dict(
#             title=dict(
#                 text=x_var
#             )
#         ),
#         yaxis=dict(
#             title=dict(
#                 text='Mass flow rate of dp at the outlet relative to the inlet'
#             )
#         ),
#         font=dict(size=16)
#     )
#     print("Writing scatter plot files...")
#     fig.write_html(directory + '/scatter/' + x_var + '.html')
#     if not os.path.isdir("Exports/scatter"):
#         os.mkdir("Exports/scatter")
#     fig.write_image(directory + '/scatter/' + x_var + '.png', format='png', scale=1, width=1000, height=1000)
#     print("Scatter plot files written.")
#     fig.show()