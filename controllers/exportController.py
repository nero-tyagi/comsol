from controllers.mphController import controller
from constants import DISPLAY_NODE_TREE
from input_files.inputVariables import MPH_FILES, EXPORT_PLOT_NODES
from functions.plots import batch_export_pgs
from os.path import exists as EXISTS
from shutil import rmtree as RMTREE

models, clients, solutions = controller(MPH_FILES, DISPLAY_NODE_TREE)
print(models)

#todo: Need to add a loop to export all the export resolution presets in 0.5x, 1x, 2x, and 4x directories

#todo: Need to add a loop to export multiple views if the user chooses to do so (usually a particular view and an
#todo: extent view.

for im, model in enumerate(models):
    overwrite = True
    current_solutions = solutions[im]
    i = 0
    for solution in current_solutions:
        print(str(i) + ": " + str(solution))
        i += 1
    if solution:
        selected_solution = -1
        print()
        selected_solution = input("Which solution would you like to choose for the plots? ")
        nomenclature = input("Prefix for the nomenclature: ")
        input_set = ["y", "n", "Y", "N"]
        while True:
            user_input = input("Overwrite solutions? y or n: ")
            if user_input in input_set:
                if user_input in ["Y", 'y']:
                    overwrite = True
                else:
                    overwrite = False
                break
            else:
                print("Wrong input. Please enter 'y' or 'n'")
        while True:
            try:
                selected_solution = int(selected_solution)
                if selected_solution >= 0:
                    if selected_solution <= len(solution):
                        break
            except ValueError:
                print("Wrong input. Please choose again.")
        node = model / 'solutions' / current_solutions[selected_solution]
        print("Solution node selected: " + str(node))
        print("Ovewrite: " + str(overwrite))
        batch_export_pgs(model,
                         overwrite,
                         node,
                         nomenclature,
                         EXPORT_PLOT_NODES)
    else:
        print("No solutions found.")