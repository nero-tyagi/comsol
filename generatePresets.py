from mphFunctions import get_node_properties
import os
from constants import *


def genProps(model, plot_groups=None, node='plots'):

    if not plot_groups:
        plot_groups = [
            model / node / 'Continuous Phase Velocity',
            model / node / 'Dispersed Phase Velocity',
            model / node / 'Pressure',
            model / node / 'Streamlines (Uc)',
            model / node / 'Separation Velocity (Ud - Uc), Arrow Surface',
            model / node / 'Dispersed Phase Volume Fraction'
        ]
    node_name = 'Plot'
    if node == 'exports':
        node_name = 'Export'
    messages = ""
    for pg in plot_groups:
        messages += (pg.name()
                     + "\n\t" + node_name + " path: " + str(pg.path)
                     + "\n\t" + node_name + " tag: " + str(pg.tag())
                     + "\n\t" + node_name + " type: " + str(pg.type())
                     + "\n")
        properties, properties_readable = get_node_properties(pg)
        with open(PRESETS_FOLDER + node + "/" + pg.name() + ".txt", "w") as file:
            file.write(str(properties))
        with open(PRESETS_FOLDER + node + "/" + "READABLE_" + pg.name() + ".txt", "w") as file:
            file.write(str(properties_readable))

        if node == 'plots':
            plots = pg.children()
            for plot in plots:
                messages += ("\n\t" + plot.name()
                             + "\n\t\t" + node_name + " path: " + str(plot.path)
                             + "\n\t\t" + node_name + " tag: " + str(plot.tag())
                             + "\n\t\t" + node_name + " type: " + str(plot.type()))
                properties, properties_readable = get_node_properties(plot)
                path = PRESETS_FOLDER + node + "/" + pg.name() + "/"
                if not os.path.exists(path):
                    os.mkdir(path)
                with open(path + plot.name() + ".txt", "w") as file:
                    file.write(str(properties))
                with open(path + "READABLE_" + plot.name() + ".txt", "w") as file:
                    file.write(str(properties_readable))

                # Generating Color Expression for streamline node
                if 'streamline' in plot.name().lower():
                    streamline_node = model / 'plots' / pg.name() / plot.name()
                    if streamline_node.children()[0]:
                        color_node = streamline_node.children()[0]
                        properties, properties_readable = get_node_properties(color_node)
                        with open(path + 'Color.txt', "w") as file:
                            file.write(str(properties))
                        with open(path + "READABLE_Color.txt", "w") as file:
                            file.write(str(properties_readable))

            messages += "\n\n"
    with open(PRESETS_FOLDER + node + "/" + "log.txt", "w") as file:
        file.write(messages)