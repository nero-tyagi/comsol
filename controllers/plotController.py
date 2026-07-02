from controllers.mphController import controller
from functions.exporting import generate_default_pgs, generate_pgs
from functions.inputs import getYOrN
from constants import PLOTGROUPS, MPH_FILES

for file in MPH_FILES:
    model, client, datasets, solutions = controller(file, False)
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
        for item in PLOTGROUPS:
            print(str(item.id) + ": " + str(item.name))

        # Getting the user's desired list of plots
        input_list = input("\nEnter a comma separated list of plots to generate. ").split(',')
        for ix, item in enumerate(input_list):
            input_list[ix] = item.replace(" ", "")
            input_list[ix] = int(input_list[ix])

        # Removing duplicates and creating the export_node list
        input_list = list(set(input_list))

        pgs = []
        for item in input_list:
            for pg in PLOTGROUPS:
                if pg.id == item:
                    pgs.append(pg.name)

        print("\nYou have chosen the following plots: ")
        for ix, item in enumerate(pgs):
            print(str(item))

        # Asking the user if they want to clear the existing plots
        clear = getYOrN("\nDo you want to clear the existing plots? ")

        # Asking the user if they want to overwrite the existing plots
        overwrite = False
        if not clear:
            overwrite = getYOrN("Do you want to overwrite the existing plots? ")

        # Generating the requested plots
        generate_pgs(model, pgs, clearPlots=clear, overwritePlots=overwrite, overwriteNodes=overwrite)