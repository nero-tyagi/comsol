from controllers.mphController import controller
from constants import DISPLAY_NODE_TREE, EXPORT_DICT
from input_files.inputVariables import MPH_FILES, EXPORT_PLOT_NODES
from functions.plots import batch_export_pgs
from functions.inputs import getYOrN
from os.path import exists as EXISTS
from shutil import rmtree as RMTREE

#todo: Improve export speed by exporting all qualities and views for a node at once
#todo: before moving on to the next node. Nodes like streamlines take a long time to
#todo: prepare for export. Preparing those plot nodes multiple times is wasteful.

default_qualities = [0.5, 1, 2, 4]

for im, file in enumerate(MPH_FILES):

    model, client, datasets, solutions = controller(file, False)
    overwrite = True
    if solutions:
        i = 0
        for solution in model.solutions():
            print(str(i) + ": " + str(solution))
            i += 1
        print()
        selected_solution = input("Which solution would you like to choose for the plots? ")
        while True:
            try:
                selected_solution = int(selected_solution)
                if selected_solution >= 0:
                    if selected_solution <= len(solutions):
                        break
            except ValueError:
                print("Wrong input. Please choose again.")
        node = model / 'solutions' / solutions[selected_solution]
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

        export_nodes = EXPORT_PLOT_NODES
        # Asking which plots to generate
        while True:
            answer = input("What plots would you like to export?\n1. Default plots\n2. Custom set of plots\n").lower()
            if answer in ['1', '2']:
                if answer == '1':
                    export_nodes = EXPORT_PLOT_NODES
                break
            else:
                print("Please enter 1 or 2.")

        print()

        for item in EXPORT_DICT:
            print(str(item) + ": " + str(EXPORT_DICT[item]))

        # Getting the user's desired list of plots
        input_list = input("\nEnter a comma separated list of plots to generate. ").split(',')
        for ix, item in enumerate(input_list):
            input_list[ix] = item.replace(" ", "")
            input_list[ix] = int(input_list[ix])

        # Removing duplicates and creating the export_node list
        input_list = list(set(input_list))
        print("\nYou have chosen the following plots: " + str(input_list))
        export_nodes = [EXPORT_DICT[x] for x in input_list]
        print(export_nodes)

        for quality in qualities:
            batch_export_pgs(model,
                             overwrite,
                             node,
                             nomenclature,
                             export_nodes,
                             quality=quality,
                             zoomextents=False,
                             view=view)
        if zoomextents_control:
            batch_export_pgs(model,
                             overwrite,
                             node,
                             nomenclature,
                             export_nodes,
                             quality=4,
                             zoomextents=True,
                             view='view1')
    else:
        print("No solutions found.")