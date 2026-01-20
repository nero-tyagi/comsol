from math import sin, cos, tan, pi
import pandas as pd
from pathlib import Path
from controllers.mphController import controller

model, client, datasets, solutions = controller("data/SDRS.mph", False)

# Model parameters
numribs = 50
rib_i = 0
r_i = 5
z_i = 0
aoa = 20 * pi / 180
theta_c = 70 * pi / 180
theta = 55 * pi / 180
h_ = 0.5
Hs = 2
H = h_ * Hs
Ws = 5
w =  h_ * Ws
r2 = r_i + h_ / sin(theta) * cos(theta + aoa)
z2 = z_i + h_ / sin(theta) * sin(theta + aoa)
r3 = r2 + cos(aoa) * w
z3 = z2 + sin(aoa) * w

df = pd.DataFrame(columns=['r', 'z', 'phid', 'udr', 'udz', 'ucr', 'ucz'])
rib_dfs = {

}

ribs_dfs = {

}
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
        Path("data")
        / "exports"
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

    df = pd.read_table(path / "outlet.txt", sep='\t', header=None)
    rib_dfs["outlet"] = df
    df = pd.read_table(path / "inlet.txt", sep='\t', header=None)
    rib_dfs["inlet"] = df
    df = pd.read_table(path / "loss.txt", sep='\t', header=None)
    rib_dfs["loss"] = df

    ribs_dfs[gap_name] = rib_dfs

model.save()