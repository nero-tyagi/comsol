from mphController import mph_import_controller
from constants import MPH_FILES, DISPLAY_NODE_TREE, EXPORT_PLOT_NODES
from exportFunctions import batch_export_Uc_plots

models, clients, solutions = mph_import_controller(MPH_FILES, DISPLAY_NODE_TREE)
print(models)
1
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
        while True:
            try:
                selected_solution = int(selected_solution)
                if selected_solution >= 0:
                    if selected_solution <= len(solution):
                        break
            except ValueError:
                print("Wrong input. Please choose again.")
        node = model / 'solutions' / current_solutions[selected_solution]
        # print(solution + ", tag: " + node.tag())
        batch_export_Uc_plots(model,
                              ['DMND', '001'],
                              EXPORT_PLOT_NODES,
                              current_solutions[selected_solution],
                              node.tag())
    else:
        print("No solutions found.")

