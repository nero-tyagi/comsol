import re
import numpy as np
from functions.mph import get_node_properties
from constants import *

# Reads the preset files and create a dictionary of preset properties
def read_presets(file):
    presets = {}

    with open(file, 'r') as f:
        content = f.read()

    # Matches each triple: ['key', value, dtype]
    pattern = re.compile(r"\['(.*?)',\s*(.*?),\s*<(.*?)>\]")
    matches = pattern.findall(content)

    for key, value_str, dtype_str in matches:
        dtype_str = dtype_str.strip()
        value_str = value_str.strip()

        if "bool" in dtype_str:
            value = value_str == "True"
        elif "int" in dtype_str:
            value = int(value_str)
        elif "float" in dtype_str or "JDouble" in dtype_str:
            value = float(value_str)
        elif "NoneType" in dtype_str:
            value = None
        elif "str" in dtype_str:
            value = value_str.strip("'\"")
        elif "list" in dtype_str:
            value = eval(value_str)  # safe for simple lists
        elif "numpy.ndarray" in dtype_str:
            # Handle empty arrays
            if value_str.startswith("array([]"):
                value = np.array([])
            else:
                # Extract contents inside array([...])
                arr_contents = re.search(r"array\((.*)\)", value_str).group(1)
                # Remove dtype=... if present
                arr_contents = re.sub(r",\s*dtype=.*", "", arr_contents)
                value = np.array(eval(arr_contents))
        else:
            value = value_str

        presets[key] = value

    return presets


# Generates files containing properties of selected plot groups in a model. These
# properties files can be used to create presets. Modify whatever is needed in these
# properties files and then move them into the presets folder.
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
        with open(PRESETS_FOLDER + "new/" + node + "/" + pg.name() + ".txt", "w") as file:
            file.write(str(properties))
        with open(PRESETS_FOLDER + "new/" + node + "/" + "READABLE_" + pg.name() + ".txt", "w") as file:
            file.write(str(properties_readable))

        if node == 'plots':
            plots = pg.children()
            for plot in plots:
                messages += ("\n\t" + plot.name()
                             + "\n\t\t" + node_name + " path: " + str(plot.path)
                             + "\n\t\t" + node_name + " tag: " + str(plot.tag())
                             + "\n\t\t" + node_name + " type: " + str(plot.type()))
                properties, properties_readable = get_node_properties(plot)
                path = PRESETS_FOLDER + "new/" + node + "/" + pg.name() + "/"
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
    with open(PRESETS_FOLDER + "new/" + node + "/" + "log.txt", "w") as file:
        file.write(messages)