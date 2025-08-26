from mphController import *
import os
from mphFunctions import *
import mph

# Defining directories
os.environ["DYLD_LIBRARY_PATH"] = "/Applications/COMSOL63/Multiphysics"
path = os.environ["DYLD_LIBRARY_PATH"]

mph_files = ['input_files/BWRD.mph']

models, clients = mph_import_controller(mph_files, False)

plots = [
    models[0]/'plots'/'Continuous Phase Velocity',
    models[0]/'plots'/'Continuous Phase Streamlines',
    models[0]/'plots'/'Dispersed Phase Velocity',
    models[0]/'plots'/'Velocity Difference (Ud - Uc), Arrow Surface',
    models[0]/'plots'/'Continuous Phase Pressure',
    models[0]/'plots'/'Dispersed Phase Volume Fraction'
]
messages = ""
for plot in plots:
    messages += (plot.name()
                 + "\n\tPlot path: " + str(plot.path)
                 + "\n\tPlot tag: " + str(plot.tag())
                 + "\n\tPlot type: " + str(plot.type())
                 + "\n")
    properties = get_node_properties(plot)
    with open("plot_presets/source_desc_values/" + plot.name() + ", " + plot.tag() + ".txt", "w") as file:
        file.write(str(properties))

    plot_children = plot.children()
    for subplot in plot_children:
        messages += ("\n\t" + subplot.name()
                     + "\n\t\tPlot path: " + str(subplot.path)
                     + "\n\t\tPlot tag: " + str(subplot.tag())
                     + "\n\t\tPlot type: " + str(subplot.type()))
        properties = get_node_properties(subplot)
        with open("plot_presets/source_desc_values/" + subplot.name() + ", " + subplot.tag() + ".txt", "w") as file:
            file.write(str(properties))
    messages += "\n\n"
with open("plot_presets/source_desc_values/log.txt", "w") as file:
    file.write(messages)

