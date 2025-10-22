from controllers.mphController import controller
from input_files.inputVariables import MPH_FILES
from input_files.inputVariables import EXPORT_PLOT_NODES
from constants import EXPORT_DICT
from functions.plots import generate_export_node, default_plots
from functions.inputs import getYOrN

# Accessing plot keys from the export_plot_nodes list using the export dictionary
plots = []
for x in EXPORT_PLOT_NODES:
    for key, val in EXPORT_DICT.items():
        if val == x:
            plots.append(key)

for file in MPH_FILES:
    model, client, datasets, solutions = controller(file, False)
    view = input("What view would you like to use? 'n' for default view. ")
    if view == 'n':
        view = 'view1'

    zoomextents_control = getYOrN("Would you like to export with ZoomExtents enabled? y or n. ")
    print("ZoomExtents: " + str(zoomextents_control))

    i = 1
    print()
    for qual in [0.5, 1, 2, 4]:
        print(str(i) + ". " + str(qual) + "x")
        i += 1

    quality = 1
    while True:
        quality = input("\nEnter the # of the quality you want to generate. ")
        try:
            quality = int(quality)
            if quality in [1, 2, 3, 4]:
                break
            else:
                print("Wrong input. Please choose again.")
        except ValueError:
            print("Wrong input. Please choose again.")
    if quality == 1:
        quality = 0.5
    elif quality == 2:
        quality = 1
    elif quality == 3:
        quality = 2
    print("Quality: " + str(quality) + "x")

    overwrite = getYOrN("Would you like to overwrite the existing export nodes? ")
    print("Overwrite: " + str(overwrite))

    for plot in plots:
        generate_export_node(model, overwrite, pg_name=default_plots.get(plot),
                             view=view,
                             quality=quality,
                             zoomextents=zoomextents_control)
        # Saving the model
        model.save()