from functions.presets import read_presets
from functions.mph import get_datasets, clearPlotGroups
from constants import *
from constants import (PNG_NAME_DICT,
                       EXPORT_DIRECTORY)
import re

# Use this list to pass an array of a combination of these numbers to generate plots
default_plots = {
    1: 'Continuous Phase Velocity',
    2: 'Dispersed Phase Velocity',
    3: 'Pressure',
    4: 'Streamlines (Uc)',
    5: 'Separation Velocity (Ud - Uc), Arrow Surface',
    6: 'Dispersed Phase Volume Fraction',
}

# Generates a plot group, populates it with plots, changes all properties to preset properties, and handles exceptions
def generate_pg(model, overwritePlots, pg_name="Continuous Phase Velocity", dset=''):

    if overwritePlots:

        # Checking to see if the plot title already exists and deleting it if it does.
        existing_plot_groups = model.plots()
        if pg_name in existing_plot_groups:
            temp_node = model/'plots'/pg_name
            try:
                temp_node.remove()
            except Exception as e:
                print("Could not delete " + pg_name)
                raise e
        plot_title = pg_name

    else:

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
    print("\nGenerated plot group: " + str(new_plot_group_node))
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

    print("Generated plot(s): " + str(str(plot.name() + " ") for plot in plot_nodes))

    # Getting plot group preset values
    print("Reading plot group preset values...")
    pg_presets = read_presets(
        file=PRESETS_FOLDER + "/plots/" + pg_name + ".txt")

    # Setting preset values, ignoring those in the ignore list
    print("Setting plot group preset values...")
    for property in pg_presets:
        if property not in PG_IGNORE_LIST:
            try:
                new_plot_group_node.property(property, pg_presets.get(property))
            except Exception as e:
                print("Could not assign property " + str(property))
                print("Property value:" + str(pg_presets.get(property)))
                # raise e

    # Getting plot preset values and setting them to the new plots, ignoring those in the ignore list
    for node in plot_nodes:
        print("Reading preset values for plot: " + node.name())
        plot_presets = read_presets(
            file=PRESETS_FOLDER + "plots/" + pg_name + "/" + node.name() + ".txt")

        print("Setting preset values for plot: " + node.name())
        for property in plot_presets:
            if property not in PLOT_IGNORE_LIST:
                try:
                    if property == "solnum":
                        print("solnum value:")
                        print(new_plot_group_node.property(property))
                    node.property(property, plot_presets.get(property))
                except Exception as e:
                    print("Could not assign property " + str(property))
                    print("Property value:" + str(plot_presets.get(property)))
                    # raise e

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

            # Creating Color Expression
            print("Creating color node")
            color_node = node.create('Color')

            # Setting Color Expression preset values
            print("Setting color expression values")
            color_presets = read_presets(
                file=PRESETS_FOLDER + "plots/" + pg_name + "/Color.txt")
            for property in color_presets:
                if property not in PLOT_IGNORE_LIST:
                    try:
                        color_node.property(property, color_presets.get(property))
                    except Exception as e:
                        print("Could not assign property " + str(property))
                        print("Property value:" + str(color_presets.get(property)))
                        # raise e
            color_node.property('colortable', color_presets.get('colortable'))
        else:
            node.property('colortable', plot_presets.get('colortable'))
        # Setting the titletype
        node.property('titletype', 'none')

        # Since plot properties do not include whether the plot is shown or hidden, this setting has to be manually
        # adjusted
        if pg_name == "Pressure":
            if node.name() == 'Surface plot':
                node.toggle()
    print()

    new_plot_group_node.property('titletype', 'none')
    new_plot_group_node.property('data', dset)

# Generates a plot group, populates it with plots, changes all properties to preset properties, and handles exceptions
def generate_export_node(model, overwriteNodes, pg_name="Continuous Phase Velocity",
                         view='view1',
                         quality=1,
                         zoomextents=False):

    if overwriteNodes:

        # Checking to see if the export node title already exists and deleting it if it does.
        existing_export_nodes = model.exports()
        if pg_name in existing_export_nodes:
            temp_node = model / 'exports' / pg_name
            try:
                temp_node.remove()
            except Exception as e:
                print("Could not delete export node " + pg_name)
                raise e
        node_title = pg_name

    else:

        # Checking to see if the export node title already exists and appending a number if so.
        node_title = pg_name
        existing_export_nodes = model.exports()
        print("\nExisting export nodes:")
        print(existing_export_nodes)
        i = 1
        name_acquired = False
        while not name_acquired:
            if node_title in existing_export_nodes:
                node_title = pg_name + " " + str(i)
            else:
                name_acquired = True
                print("Final export node name: " + node_title)
            i += 1

    # Generating the plot and the subplot
    exports_node = model / 'exports'
    exports_node.create("Image", name=node_title)
    new_export_node = model / 'exports' / node_title
    print("Generated export node: " + str(new_export_node))

    # Getting export node preset values
    print("Reading export node preset values...")
    pg_presets = read_presets(
        file=PRESETS_FOLDER + "/exports/exports.txt")

    # Setting preset values, ignoring those in the ignore list
    print("Setting export node preset values...")
    for property in pg_presets:
        if property not in EXPORT_IGNORE_LIST:
            try:
                new_export_node.property(property, pg_presets.get(property))
            except Exception as e:
                print("Could not assign property " + str(property))
                print("Property value:" + str(pg_presets.get(property)))
                # raise e

    # Setting custom export settings
    EXPORT_PRESET_1 = {
        'aspectratio': float(1.0),
        'background': 'color',
        'colortheme': 'ClassicDark',
        'customcolor': [float(0), float(0), float(0)],
        'fontsize': int(20),
        'height': float(1000.0),
        'heightmultiple': int(1),
        'heightpx': int(1000),
        'qualitylevel': int(100),
        'resolution': int(96),
        'showgrid': True,
        'sourcetype': 'plotgroup',
        'width': float(1000.0),
        'widthpx': float(1000.0)
    }
    EXPORT_PRESET_1['fontsize'] = int(EXPORT_PRESET_1['fontsize'] * quality)
    EXPORT_PRESET_1['heightpx'] = int(EXPORT_PRESET_1['heightpx'] * quality)
    EXPORT_PRESET_1['height'] = float(EXPORT_PRESET_1['height'] * quality)
    EXPORT_PRESET_1['width'] = float(EXPORT_PRESET_1['width'] * quality)
    EXPORT_PRESET_1['widthpx'] = float(EXPORT_PRESET_1['widthpx'] * quality)
    for property, value in EXPORT_PRESET_1.items():
        try:
            new_export_node.property(property, value)
        except Exception as e:
            print("Could not assign property " + str(property))
            print("Property value:" + str(value))
    new_export_node.property('zoomextents', zoomextents)

    source_node = model/'plots'/pg_name
    new_export_node.property('pngfilename', 'NOPATH.png')
    new_export_node.property('view', view)
    new_export_node.property('sourceobject', source_node.tag())

# Generates all the default plot groups using the existing presets
def generate_default_pgs(model, clearPlots=False, overwritePlots=False):

    plots = [1, 2, 3, 4, 5, 6]
    # Clearing all pre-existing plots
    if clearPlots:
        clearPlotGroups(model)
    # Selecting the last available solution or parametric solution
    # dataset node to give to plot groups
    dsets = get_datasets(model)
    dset_tag = ''
    if dsets != []:
        print(dsets)
        dset_node = model / 'datasets' / model.solutions()[0]
        dset_tag = dset_node.tag()

    for plot in plots:
        generate_pg(model, overwritePlots, pg_name=default_plots.get(plot), dset=dset_tag)
        generate_export_node(model, True, pg_name=default_plots.get(plot), view='view1')

    print("Saving model " + str(model.name()) + "...")
    model.save()
    print("Model saved. Exiting.\n")



def generate_pgs(model, pgs, clearPlots=False, overwritePlots=False, overwriteNodes=False):
    # Clearing all pre-existing plots
    if clearPlots:
        clearPlotGroups(model)
    # Selecting the last available dataset node to give to plot groups
    dsets = get_datasets(model)
    dset_tag = ''
    if dsets != []:
        dset_node = model / 'datasets' / model.solutions()[-1]
        dset_tag = dset_node.tag()
    for pg in pgs:
        generate_pg(model, overwritePlots, pg_name=pg, dset=dset_tag)
        generate_export_node(model, overwriteNodes, pg_name=pg, view='view1')

    print("Saving model " + str(model.name()) + "...")
    model.save()
    print("Model saved. Exiting.\n")



def batch_export_pgs(model, overwrite_mode, solution_node, model_name,
                     export_nodes, quality=1, zoomextents=False, view='view1'):

    print("Exporting with quality settings: Quality = " + str(quality) +
          "x and ZoomExtents = False...")
    for node in export_nodes:
        generate_export_node(model,
                             True,
                             pg_name=node,
                             view=view,
                             quality=quality,
                             zoomextents=zoomextents)

    # Using the given node to identify the outer solutions
    outer_solutions = solution_node.children()

    if not outer_solutions:
        # If no outer solutions are found, please make sure that the study actually has
        # all the results you expect.
        print("\nNo solutions found. No plots exported.")
    else:
        print("\nOuter solutions found. " + str(outer_solutions))

    # Finding the dataset that the solution node belongs to in order to assign it
    # to the pg
    dsets = model.datasets()
    dset = ""
    name = str(solution_node).split('/', 1)[1]
    for set in dsets:
        if name in set:
            dset = set
    dset_node = model / 'datasets' / dset
    dset = dset_node.tag()

    ## Batch exporting the plots:

    # Overwrite mode - If not overwriting files, first we need to find the last
    # solution number that already exists in the folder for the current model
    # name
    sol_name_i = 0 # starting solution count
    if not overwrite_mode:
        print("\nChecking existing files for the current model name...")
        try:
            files = os.listdir(EXPORT_DIRECTORY)
            # print(files)
            try:
                # Separating the files that contain only the current model's name
                files = [x for x in files if model_name in x]
                # print("Cleaned list of files: ")
                # print(files)
                max_int = 0

                # WARNING: This is sensitive to how the folders are named.
                for file in files:
                    latter_part = str(file).split(model_name + " - ", 1)[1]
                    # print("latter_part:", latter_part)

                    # Find the number before the first '['
                    match = re.search(r'(\d+)', latter_part)
                    if match:
                        number = int(match.group(1))
                        if number > max_int:
                            max_int = number
                print(max_int)
                sol_name_i = max_int
            except Exception as e:
                print(e)
        except Exception as e:
            print("No export directory found.")
            sol_name_i = 0
    else:
        print("\nOverwriting existing files...")

    sol_name_i += 1
    sol_i = 1
    for sol in outer_solutions:
        for node in export_nodes:
            plot_node = model / 'plots' / str(node)
            export_node = model / 'exports' / node
            plot_node.property('data', str(dset))
            plot_node.property('outersolnum', str(sol_i))
            model_name = model_name
            export_2D_PG(model, node, export_node, sol, sol_name_i,
                         model_name, quality, zoomextents)
        sol_i += 1
        sol_name_i += 1

    # Saving the model
    model.save()

# Export Uc plots
def export_2D_PG(model, node, export_node, sol, sol_name_i,
                 model_name, quality, zoomextents):

    # Initializing variables for the name of the png
    sol_name = sol.name()
    if node in PNG_NAME_DICT:
        file_name = PNG_NAME_DICT.get(node)
    # WARNING: Searching for the next solution count for the folder names in
    # WARNING: non overwrite mode of exporting plots depends on this folder
    # WARNING: nomenclature. DO NOT CHANGE

    export_directory_i = (("exports/" + model_name +
                          " - " + str(sol_name_i) + " [" + sol_name) + "]" +
                          "/" + str(quality) + "x")
    export_file_name = export_directory_i + '/' + file_name
    if zoomextents:
        export_file_name += "_zoomextents"
    if node in PNG_NAME_DICT:
        export_file_name += ".png"

    print("Exporting node \"" + str(node) + "\" as " + export_file_name)
    try:
        if node in PNG_NAME_DICT:
            model.export(export_node, file=export_file_name)
            print("Exported: " + export_file_name)
        else:
            print("Couldn't find a suitable name for this plot group.")
    except Exception as e:
        print("Could not export: " + export_file_name)
        print(e)
