from controllers.mphController import controller
from input_files.inputVariables import MPH_FILES
from functions.plots import generate_default_pgs, generate_pgs
from functions.inputs import getYOrN
from constants import EXPORT_DICT

for file in MPH_FILES:
    model, client, datasets = controller(file, False)
    print("Generating export nodes in model " + str(model.name()) + "\n")

    while True:
        answer = input("What plots would you like to generate?\n1. Default plots\n2. Custom set of plots\n").lower()
        if answer in ['1', '2']:
            if answer == '1':
                # WARNING: The following code overwrites the default plots.
                generate_default_pgs(model, overwritePlots=True)
            break
        else:
            print("Please enter 1 or 2.")

    if answer == '2':
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
        pgs = [EXPORT_DICT[x] for x in input_list]
        print(pgs)

        # Asking the user if they want to clear the existing plots
        clear = getYOrN("\nDo you want to clear the existing plots? ")

        # Asking the user if they want to overwrite the existing plots
        overwrite = False
        if not clear:
            overwrite = getYOrN("Do you want to overwrite the existing plots? ")

        # Generating the requested plots
        generate_pgs(model, pgs, clearPlots=clear, overwritePlots=overwrite, overwriteNodes=overwrite)