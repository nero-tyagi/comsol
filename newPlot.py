import ast
import re
import numpy as np
import math

preset_plots = {
    1: 'Continuous Phase Velocity',
    2: 'Dispersed Phase Velocity',
    3: 'Pressure',
    4: 'Streamlines (Uc)',
    5: 'Separation Velocity (Ud - Uc), Arrow Surface',
    6: 'Dispersed Phase Volume Fraction',
}

def generate_pg(model, pg_name="Continuous Phase Velocity"):

    pg_ignore_list = [
        'data',
        'looplevel',
        'outersolnum',
        'outertype',
        'solnum',
        'solrepresentation',
        'solutionparams',
        'title'
    ]

    plot_ignore_list = [
        'actuallevels',
        'actuallevelslegend',
        'labels',
        'outersolnum',
        'outertype',
        'plotinfo',
        'rangeactualminmax',
        'rangecolormax',
        'rangecolormin',
        'rangedatamax',
        'rangedatamin',
        'rangeminpositive',
        'rangeunit',
        'rowindex',
        'solnum',
        'title',
        'unit',
    ]
    # Checking to see if the plot title already exists and appending a number if so.
    plot_title = pg_name
    existing_plot_groups = model.plots()
    print("\nExisting plot groups:")
    print(existing_plot_groups)
    i = 1
    name_acquired = False
    while not name_acquired:
        if plot_title in existing_plot_groups:
            plot_title = pg_name + " " + str(i)
        else:
            name_acquired = True
            print("Final plot name: " + plot_title)
        i += 1

    # Generating the plot and the subplot
    plot_groups_node = model/'plot'
    plot_groups_node.create("PlotGroup2D", name=plot_title)
    new_plot_group_node = model/'plot'/plot_title
    plot_nodes = []

    # Selecting the appropriate subplot depending on the type of the plot
    if "Streamlines".lower() in pg_name.lower():
        new_plot_group_node.create("Streamline", name="Streamlines")
        plot_nodes.append(new_plot_group_node / "Streamlines")
    elif "Arrow Surface".lower() in pg_name.lower():
        new_plot_group_node.create("Surface", name="Surface plot")
        new_plot_group_node.create("ArrowSurface", name="Arrow surface plot")
        plot_nodes.append(new_plot_group_node / "Surface plot")
        plot_nodes.append(new_plot_group_node / "Arrow surface plot")
    elif "Pressure".lower() in pg_name.lower():
        new_plot_group_node.create("Surface", name="Surface plot")
        new_plot_group_node.create("Contour", name="Contour plot")
        plot_nodes.append(new_plot_group_node / "Surface plot")
        plot_nodes.append(new_plot_group_node / "Contour plot")
    else:
        new_plot_group_node.create("Surface", name="Surface plot")
        plot_nodes.append(new_plot_group_node / "Surface plot")

    # Getting plot group preset values
    print("Reading plot group preset values")
    pg_presets = read_presets(
        file="plot_presets/source_desc_values/" + pg_name + ".txt")
    print(pg_presets)
    # Setting preset values, ignoring those in the ignore list
    print("Setting plot group preset values")
    for property in pg_presets:
        if property not in pg_ignore_list:
            try:
                new_plot_group_node.property(property, pg_presets.get(property))
            except Exception as e:
                print("Could not assign property " + str(property))
                print("Property value:" + str(pg_presets.get(property)))
                raise e

    # Getting plot preset values and setting them to the new plots, ignoring those in the ignore list
    for node in plot_nodes:
        print("Reading " + node.name() + " preset values")
        plot_presets = read_presets(
            file="plot_presets/source_desc_values/" + pg_name + "/" + node.name() + ".txt")

        print("Setting " + node.name() + " preset values")
        for property in plot_presets:
            if property not in plot_ignore_list:
                try:
                    node.property(property, plot_presets.get(property))
                except Exception as e:
                    print("Could not assign property " + str(property))
                    print("Property value:" + str(plot_presets.get(property)))
                    raise e

        # Handling excpetions:

        # There is probably a correct order of applying the properties, and for some reason, the colortable and some
        # other properties do not apply properly if done in the order of the preset file. Hence, these two properties
        # need to be changed again afterward.

        if "arrow" in node.name().lower():
            break
        elif "contour" in node.name().lower():
            node.property('colortable', plot_presets.get('colortable'))
        elif "streamline" in node.name().lower():
            node.property('linetype', 'line')
        else:
            node.property('colortable', plot_presets.get('colortable'))
        # Setting the titletype
        node.property('titletype', 'none')

        # Since plot properties do not include whether the plot is shown or hidden, this setting has to be manually
        # adjusted
        if pg_name == "Pressure":
            if node.name() == 'Surface plot':
                node.toggle()

    new_plot_group_node.property('titletype', 'none')

    # Saving the model
    model.save()

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