from controllers.mphController import controller
from constants import MPH_FILES, DISPLAY_NODE_TREE, EXPORT_PLOT_NODES
from functions.plots import batch_export_pgs
from os.path import exists as EXISTS
from shutil import rmtree as RMTREE

models, clients, solutions = controller(MPH_FILES, DISPLAY_NODE_TREE)
print(models)

# Remove all the files in all the subdirectories and files inside "Exports"
def clear_exports():
    if EXISTS("Exports"):
        RMTREE("Exports")

for im, model in enumerate(models):
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
        batch_export_pgs(model,
                              node,
                              [nomenclature, '001'],
                              EXPORT_PLOT_NODES)
    else:
        print("No solutions found.")

