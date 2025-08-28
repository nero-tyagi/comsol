import ast
import re

def continuous_phase_velocity(model, plot_name="Continuous Phase Velocity"):

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

    surface_ignore_list = [
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
        'unit'
    ]
    # Checking to see if the plot title already exists and appending a number if so.
    plot_title = plot_name
    existing_plots = model.plots()
    i = 1
    name_acquired = False
    while not name_acquired:
        if plot_title in existing_plots:
            plot_title = plot_name + " " + str(i)
        else:
            name_acquired = True
            print("Final plot name: " + plot_title)
        i += 1

    # Generating the plot and the subplot
    plots_node = model/'plot'
    plots_node.create("PlotGroup2D", name=plot_title)
    plot_node = model/'plot'/plot_title
    plot_node.create("Surface", name="Surface plot")
    subplot_node = plot_node/"Surface plot"

    # Getting preset values
    pg_presets = read_presets(
        file="plot_presets/source_desc_values/Continuous Phase Velocity, pg11.txt")
    surface_presets = read_presets(
        file="plot_presets/source_desc_values/Velocity Magnitude, Continuous Phase, surf1.txt")

    # Setting preset values, ignoring tthose in the ignore list
    for property in pg_presets:
        if property[0] not in pg_ignore_list:
            plot_node.property(property[0], property[1])
    for property in surface_presets:
        if property[0] not in surface_ignore_list:
            subplot_node.property(property[0], property[1])

    # There is probably a correct order of applying the properties, and for some reason, the colortable and title does
    # not properly apply if done in the order of the preset file. Hence, these two properties need to be changed again
    # afterward.

    # Finding and setting the colortable
    for property in surface_presets:
        if property[0] == 'colortable':
            subplot_node.property('colortable', property[1])
    # Setting the titletype
    plot_node.property('titletype', 'none')

    # Saving the model
    model.save()

def read_presets(file):
    with open(file) as f:

        raw = f.read()

        # --- Step 1: remove arrays with dtype ---
        # array([], dtype=float64) -> []
        cleaned = re.sub(r"array\(\s*\[?\s*\]?\s*,\s*dtype=[^)]+\)", "[]", raw)

        # --- Step 2: arrays with values ---
        # array([0.05, 1.5]) -> [0.05, 1.5]
        cleaned = re.sub(r"array\((\[[^\]]*\])\)", r"\1", cleaned)

        # --- Step 3: catch simpler forms like array([0.]) or array([]) ---
        cleaned = re.sub(r"array\((.*?)\)", r"\1", cleaned)

        # Converting into a Python object
        data = ast.literal_eval(cleaned)
        # Extracting the first two elements
        array_2d = [[row[0], row[1]] for row in data]
        return array_2d