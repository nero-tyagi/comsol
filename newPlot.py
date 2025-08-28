# models[0].save()
import ast
import re

def continuous_phase_velocity(model, plot_name="Continuous Phase Velocity"):

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

    # Reading preset values
    with open("plot_presets/source_desc_values/Continuous Phase Velocity, pg11.txt") as f:

        raw = f.read()

        # --- Replace numpy arrays with plain lists ---
        cleaned = re.sub(r"array\((\[.*?\])\)", r"\1", raw)
        # array([], dtype=float64) -> []
        cleaned = re.sub(r"array\(\s*\[?\s*\]?\s*,\s*dtype=[^)]+\)", "[]", cleaned)
        # array([0.]) or array([]) -> [] or [0.]
        cleaned = re.sub(r"array\((.*?)\)", r"\1", cleaned)

        # Converting into a Python object
        data = ast.literal_eval(cleaned)
        # Extracting the first two elements
        array_2d = [[row[0], row[1]] for row in data]
        print(array_2d[:10])