import os
import shutil
from main import (png_name_dict,
                  data_name_dict,
                  export_outer_sol_required,
                  change_plot_or_export, export_directory)
import numpy as np


# Remove all the files in all the subdirectories and files inside "Exports"
def clear_exports():
    if os.path.exists("Exports"):
        shutil.rmtree("Exports")

def batch_export_Uc_plots(model, model_name_array, export_nodes):

    # Generating a list of all the solutions available and their tags.
    solution_tags = {}
    print("Solutions:")
    for solution in model.solutions():
        node = model / 'solutions' / solution
        print(solution + ", tag: " + node.tag())
        solution_tags[solution] = node.tag()

    # Finding the parametric solutions node and using that to identify the outer solutions
    sol_node = model / 'solutions' / 'Parametric Solutions 1'
    outer_solutions = sol_node.children()

    if not outer_solutions:
        # If not outer solutions are found, please make sure that the study actually has
        # all the results you expect.
        print("\nNo solutions found. No plots exported.")
    else:
        print("\nOuter solutions found. " + str(outer_solutions))

    # Batch exporting the plots:
    sol_i = 1
    for sol in outer_solutions:

        for node in export_nodes:
            if str(node) in change_plot_or_export:
                if change_plot_or_export.get(str(node)) == 'export':
                    plot_node = model / 'export' / str(node)
                elif change_plot_or_export.get(str(node)) == 'plot':
                    plot_node = model / 'plots' / str(node)
            print(plot_node)

            # print("plot_node_properties before change: ")
            # for node_property in plot_node.properties().items():
            #     print(node_property)

            if export_outer_sol_required.get(node):
                solnum = (solution_tags.get('Parametric Solutions 1'))[-1]
                # for x in plot_node.properties():
                #     print(str(x))
                # if change_plot_or_export.get(str(node)) == 'plot':
                #         plot_node.property('solnum', solnum)

            # print("plot_node_properties after change: ")
            # for node_property in plot_node.properties().items():
            #     print(node_property)

            print("\nExporting node: " + node)
            export_node = model / 'exports' / node

            # Setting the outer solution number and the name of the file
            if export_outer_sol_required.get(node):
                print("Changing solnum")
                if change_plot_or_export.get(str(node)) == 'plot':
                    plot_node.property('outersolnum', sol_i)
                elif change_plot_or_export.get(str(node)) == 'export':
                    plot_node.property('outersolnumindices', [sol_i])

            model_name = model_name_array[0]

            export_Uc_plot(model, node, plot_node, export_node, sol, sol_i, model_name)
        sol_i = sol_i + 1

# Export Uc plots
def export_Uc_plot(model, node, plot_node, export_node, sol, sol_count, model_name):

    if not os.path.isdir("Exports"):
        os.mkdir("Exports")

    # Initializing variables for the name of the png
    sol_name = sol.name()
    if node in png_name_dict:
        file_name = png_name_dict.get(node)
    elif node in data_name_dict:
        file_name = data_name_dict.get(node)
    else:
        file_name = "unknown"
    export_directory_i = export_directory + model_name + "- "+ sol_name
    if not os.path.exists(export_directory_i):
        os.mkdir(export_directory_i)
    export_file_name = export_directory + model_name + "- "+ sol_name + '/' + file_name
    if node in png_name_dict:
        export_file_name += ".png"
    elif node in data_name_dict:
        export_file_name += ".txt"

    print("Exporting: " + export_file_name )
    try:
        if node in png_name_dict:
            model.export(export_node, file=export_file_name)
            print("Exported: " + export_file_name)
        elif node in data_name_dict:
            model.export(export_node, file=export_file_name)
            print("Exported: " + export_file_name)

    except:
        if node in png_name_dict:
            print("Exported: " + export_file_name)
        elif node in data_name_dict:
            print("Exported: " + export_file_name)
