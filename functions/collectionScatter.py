import plotly.express as px
import pandas as pd
import numpy as np
import os
from constants import EXPORT_DIRECTORY, CM_FILE

# Labels in Unicode
labels_dict = {
    'aoa': 'AoA',
    'Hs': 'Hs',
    'Ws': 'Ws',
    'Name': 'Model name',
    'Cm_dot': 'Ċₘ',
    'mdot': 'ṁ',
    'theta': 'θ',
    'theta_c': 'θᶜ'
}

# Generate the scatter plot
def create_mass_flow_scatter(size=1, resolution=1):

    # This dictionary is used to give titles to the variables in the columns of the dataframe
    df_dict = {
        'Name': 'Model name',
        'Ws': 'Width-height ratio (w:h)',
        'Hs': 'Gap-height ratio (H:h)',
        'theta': 'Coupon angle',
        'aoa': 'Angle of attack',
        'theta_c': 'Cone angle',
        'mdot': 'Outlet mass flow rate',
        'Cm_dot': 'Dispersed phase mass flow rate ratio (outlet/mean %)'
    }

    df = pd.read_excel(CM_FILE, names=list(df_dict.keys()))
    print(df)
    df = df[df["Cm_dot"] > 0]

    # Plotting variables
    x_var = 'Ws'
    color_var = 'aoa'
    size_var = 'Cm_dot'
    symbol_var = 'theta_c'
    y_var = 'Hs'

    # Editing the dataframe
    df[color_var] = df[color_var].astype(str)
    df['Cm_dot'] = round(df['Cm_dot'] * 100, 1)
    df['mdot'] = ["{:.2e}".format(x) for x in df['mdot']]

    # Creating the figure
    fig = px.scatter(df,
                     x=x_var,
                     y=y_var,
                     color=color_var,
                     size=size_var,
                     symbol=symbol_var,
                     size_max=40,
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     labels=labels_dict,
                     hover_data=df.columns
                     )

    # Editing the layout
    fig.update_layout(
        xaxis=dict(
            color='white',
            linecolor="white"
        ),
        yaxis=dict(
            color='white',
            linecolor="white",
            title=labels_dict[y_var]
        ),
        font=dict(size=16 * size),
        template='plotly_dark',
        legend=dict(itemsizing='constant'),
        showlegend=True,
    )

    # Adding annotation to explain the size variable
    fig.add_annotation(
        text=str(labels_dict[size_var]) + " is represented by the size of the bubble.",
        xref="paper", yref="paper",
        x=0.02, y=1.02,
        xanchor="left", yanchor="bottom",
        showarrow=False,
        font=dict(size=16 * size)
    )

    # Saving the figure
    print("Writing scatter plot files...")
    if not os.path.isdir(EXPORT_DIRECTORY):
        os.mkdir(EXPORT_DIRECTORY)
    if not os.path.isdir(EXPORT_DIRECTORY + "scatter/"):
        try:
            os.mkdir(EXPORT_DIRECTORY + "scatter/")
        except Exception:
            print("Failed to create directory")
    filename = ("x=" + x_var + ", " +
                "color=" + color_var +", " +
                "size=" + size_var + ", " +
                "symbol=" + symbol_var)
    fig.write_html(EXPORT_DIRECTORY + 'scatter/' + filename + '.html',
                   include_mathjax='cdn')
    fig.write_image(EXPORT_DIRECTORY + 'scatter/' + filename + '.png',
                    format='png',
                    scale=resolution,
                    width=1000,
                    height=1000)
    print("Scatter plot files saved.")

# Function to integrate the phid value over the outlet line plot to get the total dispersed phase flow rate
def calc_mdot():
    column_names = ['r', 'Hs', 'theta', 'theta_c', 'aoa',  'phid', 'udz']
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