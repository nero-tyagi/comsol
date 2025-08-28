from mphFunctions import get_node_properties
import os
from constants import *

def readAndExportPlotDescs(model):

    plot_groups = [
        model/'plots'/'Continuous Phase Velocity',
        model/'plots'/'Dispersed Phase Velocity',
        model/'plots'/'Pressure',
        model/'plots'/'Streamlines (Uc)',
        model/'plots'/'Separation Velocity (Ud - Uc), Arrow Surface',
        model/'plots'/'Dispersed Phase Volume Fraction'
    ]
    messages = ""
    for pg in plot_groups:
        messages += (pg.name()
                     + "\n\tPlot path: " + str(pg.path)
                     + "\n\tPlot tag: " + str(pg.tag())
                     + "\n\tPlot type: " + str(pg.type())
                     + "\n")
        properties, properties_readable = get_node_properties(pg)
        with open(new_presets_folder + pg.name() + ".txt", "w") as file:
            file.write(str(properties))
        with open(new_presets_folder + "READABLE_" + pg.name() + ".txt", "w") as file:
            file.write(str(properties_readable))

        plots = pg.children()
        for plot in plots:
            messages += ("\n\t" + plot.name()
                         + "\n\t\tPlot path: " + str(plot.path)
                         + "\n\t\tPlot tag: " + str(plot.tag())
                         + "\n\t\tPlot type: " + str(plot.type()))
            properties, properties_readable = get_node_properties(plot)
            path = new_presets_folder + pg.name() + "/"
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path + plot.name() + ".txt", "w") as file:
                file.write(str(properties))
            with open(path + "READABLE_" + plot.name() + ".txt", "w") as file:
                file.write(str(properties_readable))

            # Generating Color Expression for streamline node
            if 'streamline' in plot.name().lower():
                streamline_node = model/'plots'/pg.name()/plot.name()
                if streamline_node.children()[0]:
                    color_node = streamline_node.children()[0]
                    properties, properties_readable = get_node_properties(color_node)
                    with open(path + 'Color.txt', "w") as file:
                        file.write(str(properties))
                    with open(path + "READABLE_Color.txt", "w") as file:
                        file.write(str(properties_readable))

        messages += "\n\n"
    with open(new_presets_folder + "log.txt", "w") as file:
        file.write(messages)