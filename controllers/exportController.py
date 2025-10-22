from controllers.mphController import controller
from constants import DISPLAY_NODE_TREE
from input_files.inputVariables import MPH_FILES, EXPORT_PLOT_NODES
from functions.plots import batch_export_pgs
from functions.inputs import getYOrN
from os.path import exists as EXISTS
from shutil import rmtree as RMTREE

models, clients, solutions = controller(MPH_FILES, DISPLAY_NODE_TREE)
print(models)

default_qualities = [0.5, 1, 2, 4]

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
        nomenclature = input("Prefix for the nomenclature: ")
        overwrite = getYOrN("Would you like to overwrite the existing image files? ")
        print("Ovewrite: " + str(overwrite))

        view = input("What view would you like to use? 'n' for default view. ")
        if view == 'n':
            view = 'view1'
        if input("Current quality set: 0.5x, 1x, 2x, 4x."
                 " Would you like to keep it? y or n. ").lower() == 'n':
            i = 1
            print()
            for qual in [0.5, 1, 2, 4]:
                print(str(i) + ". " + str(qual) + "x")
                i += 1
            qualities = input("\nEnter a comma separated list of the # of the quality you want to generate. ").split(',')
            for ix, item in enumerate(qualities):
                qualities[ix] = item.replace(" ", "")
                qualities[ix] = int(qualities[ix])
                if qualities[ix] == 1:
                    qualities[ix] = 0.5
                elif qualities[ix] == 2:
                    qualities[ix] = 1
                elif qualities[ix] == 3:
                    qualities[ix] = 2
        else:
            qualities = default_qualities
        zoomextents_control = getYOrN("Would you like to export with ZoomExtents enabled? y or n. ")
        for quality in qualities:
            batch_export_pgs(model,
                             overwrite,
                             node,
                             nomenclature,
                             EXPORT_PLOT_NODES,
                             quality=quality,
                             zoomextents=False,
                             view=view)
        if zoomextents_control:
            batch_export_pgs(model,
                             overwrite,
                             node,
                             nomenclature,
                             EXPORT_PLOT_NODES,
                             quality=4,
                             zoomextents=True,
                             view='view1')
    else:
        print("No solutions found.")