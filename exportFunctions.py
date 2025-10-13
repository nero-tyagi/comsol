import os
import shutil
from constants import (PNG_NAME_DICT,
                       EXPORT_OUTER_SOL_REQUIRED,
                       EXPORT_DIRECTORY)
import numpy as np

# Remove all the files in all the subdirectories and files inside "Exports"
def clear_exports():
    if os.path.exists("Exports"):
        shutil.rmtree("Exports")

def batch_export_Uc_plots(model, model_name_array, export_nodes, input_solution='', solution_tag=''):

    # Generating a list of all the solutions available and their tags.
    solution_tags = {}
    print("Solutions:")
    # for solution in model.solutions():
    #     node = model / 'solutions' / solution
    #     print(solution + ", tag: " + node.tag())
    #     solution_tags[solution] = node.tag()

    # Finding the parametric solutions node and using that to identify the outer solutions
    sol_node = model / 'solutions' / input_solution
    print(sol_node)
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
            plot_node = model / 'plots' / str(node)
            export_node = model / 'exports' / node
            plot_node.property('outersolnum', sol_i)
            model_name = model_name_array[0]
            export_Uc_plot(model, node, plot_node, export_node, sol, sol_i, model_name)


            # if str(node) in change_plot_or_export:
            #     if change_plot_or_export.get(str(node)) == 'export':
            #         plot_node = model / 'export' / str(node)
            #     elif change_plot_or_export.get(str(node)) == 'plot':
            #
            # print(plot_node)
            #
            # # print("plot_node_properties before change: ")
            # # for node_property in plot_node.properties().items():
            # #     print(node_property)
            #
            # if export_outer_sol_required.get(node):
            #     solnum = (solution_tags.get('Parametric Solutions 1'))[-1]
            #     # for x in plot_node.properties():
            #     #     print(str(x))
            #     # if change_plot_or_export.get(str(node)) == 'plot':
            #     #         plot_node.property('solnum', solnum)
            #
            # # print("plot_node_properties after change: ")
            # # for node_property in plot_node.properties().items():
            # #     print(node_property)
            #
            # print("\nExporting node: " + node)
            # export_node = model / 'exports' / node
            #
            # # Setting the outer solution number and the name of the file
            # if EXPORT_OUTER_SOL_REQUIRED.get(node):
            #     print("Changing solnum")
            #     if change_plot_or_export.get(str(node)) == 'plot':
            #         plot_node.property('outersolnum', sol_i)
            #     elif change_plot_or_export.get(str(node)) == 'export':
            #         plot_node.property('outersolnumindices', [sol_i])
            #
            # model_name = model_name_array[0]
            #
            # export_Uc_plot(model, node, plot_node, export_node, sol, sol_i, model_name)
        sol_i = sol_i + 1

# Export Uc plots
def export_Uc_plot(model, node, plot_node, export_node, sol, sol_count, model_name):

    if not os.path.isdir("Exports"):
        os.mkdir("Exports")

    # Initializing variables for the name of the png
    sol_name = sol.name()
    if node in PNG_NAME_DICT:
        file_name = PNG_NAME_DICT.get(node)
    # elif node in data_name_dict:
    #     file_name = data_name_dict.get(node)
    # else:
    #     file_name = "unknown"
    export_directory_i = EXPORT_DIRECTORY + model_name + "- "+ sol_name
    if not os.path.exists(export_directory_i):
        os.mkdir(export_directory_i)
    export_file_name = EXPORT_DIRECTORY + model_name + "- "+ sol_name + '/' + file_name
    if node in PNG_NAME_DICT:
        export_file_name += ".png"

    print("Exporting: " + export_file_name )
    try:
        if node in PNG_NAME_DICT:
            model.export(export_node, file=export_file_name)
            print("Exported: " + export_file_name)
        # elif node in data_name_dict:
        #     model.export(export_node, file=export_file_name)
        #     print("Exported: " + export_file_name)

    except:
        if node in PNG_NAME_DICT:
            print("Exported: " + export_file_name)
        # elif node in data_name_dict:
        #     print("Exported: " + export_file_name)
