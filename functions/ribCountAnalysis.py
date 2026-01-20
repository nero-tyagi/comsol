from math import sin, cos, tan, pi
import pandas as pd
from pathlib import Path
from controllers.mphController import controller
import plotly.express as px

def ribCountAnalysis():
    model, client, datasets, solutions = controller("data/SDRS.mph", False)

    # Model parameters
    numribs = 50
    r_i = 5
    z_i = 0
    aoa = 20 * pi / 180
    theta_c = 70 * pi / 180
    theta = 55 * pi / 180
    h_ = 0.5
    Hs = 2
    H = h_ * Hs
    Ws = 5
    w = h_ * Ws
    r2 = r_i + h_ / sin(theta) * cos(theta + aoa)
    z2 = z_i + h_ / sin(theta) * sin(theta + aoa)
    r3 = r2 + cos(aoa) * w
    z3 = z2 + sin(aoa) * w

    cols = ['r', 'z', 'phid', 'udr', 'udz', 'ucr', 'ucz']
    rib_dfs = {}
    ribs_dfs = {}
    gap_loss_data = []

    # Iterating over the ribs
    for i in range(numribs - 1):

        gap_num = 49 - i
        gap_name = "gap_" + str(gap_num)

        # Finding cutline points
        r_inlet = [0,
                   r_i + (i + 1) * (H + h_) / sin(theta_c - aoa) * cos(theta_c)]
        z_inlet = [z_i + (i + 1) * (H + h_) / sin(theta_c - aoa) * sin(theta_c),
                   z_i + (i + 1) * (H + h_) / sin(theta_c - aoa) * sin(theta_c)]
        r_outlet = [0,
                    r_i + i * (H + h_) / sin(theta_c - aoa) * cos(theta_c)]
        z_outlet = [z_i + i * (H + h_) / sin(theta_c - aoa) * sin(theta_c),
                    z_i + i * (H + h_) / sin(theta_c - aoa) * sin(theta_c)]
        r_loss = [r3 + i * (H + h_) / sin(theta_c - aoa) * cos(theta_c),
                  r3 + i * (H + h_) / sin(theta_c - aoa) * cos(theta_c)]
        z_loss = [z3 + i * (H + h_) / sin(theta_c - aoa) * sin(theta_c),
                  z3 + H / cos(aoa) + i * (H + h_) / sin(theta_c - aoa) * sin(theta_c)]

        inlet_points = [str(r_inlet[0]), str(z_inlet[0])], [str(r_inlet[1]), str(z_inlet[1])]
        outlet_points = [str(r_outlet[0]), str(z_outlet[0])], [str(r_outlet[1]), str(z_outlet[1])]
        loss_points = [str(r_loss[0]), str(z_loss[0])], [str(r_loss[1]), str(z_loss[1])]

        print(inlet_points)
        inlet_node = model / 'datasets' / 'inlet'
        inlet_node.property('genpoints', inlet_points)
        print(outlet_points)
        outlet_node = model / 'datasets' / 'outlet'
        outlet_node.property('genpoints', outlet_points)
        print(loss_points)
        loss_node = model / 'datasets' / 'loss'
        loss_node.property('genpoints', loss_points)

        export_cutlines_node = model / 'exports' / 'Cutlines'
        export_cutlines_data_node = model / 'exports' / 'CutlinesData'
        print(export_cutlines_data_node.properties())

        # print(export_cutlines_node.properties())
        path = (
                Path("exports")
                / "ribs_data"
                / gap_name
        )
        path.mkdir(parents=True, exist_ok=True)

        print("Exporting files for gap " + gap_name)
        try:
            export_cutlines_data_node.property('data', 'cln1')
            model.export(export_cutlines_data_node, file=path / "outlet.txt")
            export_cutlines_data_node.property('data', 'cln2')
            model.export(export_cutlines_data_node, file=path / "inlet.txt")
            export_cutlines_data_node.property('data', 'cln3')
            model.export(export_cutlines_data_node, file=path / "loss.txt")
            model.export(export_cutlines_node, file=path / "cutlines.png")
            print("Exported: " + str(path / "cutlines.png"))
        except Exception as e:
            print("Could not export")
            print(e)

        path = (
                Path("data")
                / "exports"
                / "ribs_data"
                / gap_name
        )
        df = pd.read_table(path / "outlet.txt", sep='\t', header=None, names=cols)
        rib_dfs["outlet"] = df
        df = pd.read_table(path / "inlet.txt", sep='\t', header=None, names=cols)
        rib_dfs["inlet"] = df
        df = pd.read_table(path / "loss.txt", sep='\t', header=None, names=cols)
        rib_dfs["loss"] = df

        ribs_dfs[gap_name] = rib_dfs

        if gap_name == "gap_47":
            print(ribs_dfs[gap_name]['outlet'].iloc[0])

        mdot = []
        for i in range(1, len(rib_dfs['outlet']['r'])):
            mdot.append((2 * pi *
                         ((rib_dfs['outlet']['r'].iloc[i])) / 100 *
                         ((rib_dfs['outlet']['r'].iloc[i]) - (rib_dfs['outlet']['r'].iloc[i - 1])) / 100 *
                         (-1 * rib_dfs['outlet']['udz'].iloc[i]) *
                         1200 *
                         rib_dfs['outlet']['phid'].iloc[i] / 1E6))
        outlet_flow_rate = sum(mdot)

        mdot = []
        for i in range(1, len(rib_dfs['inlet']['r'])):
            mdot.append((2 * pi *
                         ((rib_dfs['inlet']['r'].iloc[i])) / 100 *
                         ((rib_dfs['inlet']['r'].iloc[i]) - (rib_dfs['inlet']['r'].iloc[i - 1])) / 100 *
                         (-1 * rib_dfs['inlet']['udz'].iloc[i]) *
                         1200 *
                         rib_dfs['inlet']['phid'].iloc[i] / 1E6))
        inlet_flow_rate = sum(mdot)

        mdot = []
        avg_loss_v = []
        for i in range(1, len(rib_dfs['loss']['z'])):
            mdot.append((2 * pi *
                         ((rib_dfs['loss']['r'].iloc[i])) / 100 *
                         ((rib_dfs['loss']['z'].iloc[i]) - (rib_dfs['loss']['z'].iloc[i - 1])) / 100 *
                         (-1 * rib_dfs['loss']['udr'].iloc[i]) *
                         1200 *
                         rib_dfs['loss']['phid'].iloc[i] / 1E6))
            avg_loss_v.append(rib_dfs['loss']['udr'].iloc[i])
        loss_flow_rate = sum(mdot)
        avg_loss_v = sum(avg_loss_v) / len(avg_loss_v)

        gap_loss_data.append({
            'gap': gap_num,
            'gap_name': gap_name,
            'inlet_flow_rate': inlet_flow_rate,
            'outlet_flow_rate': outlet_flow_rate,
            'loss_flow_rate': loss_flow_rate,
            'avg_loss_v': avg_loss_v})

        # Plotting variables
        plot_size = 2

        # Creating the figure
        fig = px.scatter(gap_loss_data,
                         x='gap',
                         y='loss_flow_rate',
                         size_max=40,
                         color_discrete_sequence=px.colors.qualitative.Plotly,
                         hover_data=gap_loss_data
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
            ),
            font=dict(size=16 * plot_size),
            template='plotly_dark',
            legend=dict(itemsizing='constant'),
            showlegend=True,
        )

        # Saving the figure
        path = (
                Path("data")
                / "exports"
                / "ribs_data"
        )
        print("Writing scatter plot files...")

        filename = "loss_analysis.png"
        fig.write_image((path / filename),
                        format='png',
                        scale=plot_size,
                        width=1000,
                        height=1000)
        print("Scatter plot files saved.")

    pd.DataFrame(gap_loss_data).to_csv('data/rib_count_analysis.csv', mode='a', header=False)
    model.save()