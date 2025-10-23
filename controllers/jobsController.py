from options.parsers.jobs import parse_jobs, expand_jobs
from constants import JOBS_PATH
from mphController import controller
from functions.exporting import generate_pgs, generate_export_node, export_2D_PG
import re
from os import listdir as listdir
from constants import EXPORT_DIRECTORY
import tkinter as tk
from tkinter import ttk

jobs = parse_jobs(JOBS_PATH)

print("Plot groups catalog:")
for pid, name in sorted(jobs.plot_groups_catalog.items()):
    print(f"{pid}: {name}")

print("Jobs:")
total_jobs = 0
for i, combo in enumerate(expand_jobs(jobs)):
    mph, regen, sol, view, pid, pg_name, q = combo
    print(f"- {mph} | {sol} | {view} | PG#{pid} ({pg_name}) | quality={q}")
    total_jobs += 1
print()
print("Total number of jobs: " + str(total_jobs))
print()

# Iterating over workItems, then over the pgs within each workItem node,
# and then over the solutions and qualities for each plot group.

plot_groups_catalog = jobs.plot_groups_catalog

jobs_done = 0

# Opening up a progress bar:
# --- tiny progress window ---
root = tk.Tk()
root.title("Export progress")
root.resizable(False, False)

count_var = tk.StringVar(value="0%")
ttk.Label(root, textvariable=count_var).grid(row=0, column=0, padx=12, pady=(12, 6))

progress_var = tk.IntVar(value=0)
pb = ttk.Progressbar(root, orient="horizontal", mode="determinate",
                     maximum=total_jobs, variable=progress_var, length=360)
pb.grid(row=1, column=0, padx=12, pady=(0, 12))

# Show the window immediately
root.update_idletasks()
root.update()

# Iterating over the work items
for workItem in jobs.work_items:

    print(f"- {workItem.mph_file} |")
    # Loading the model within each work item
    mph_file_name = "data/"
    mph_file_name += workItem.mph_file
    mph_file_name += ".mph"
    model, client, datasets, solutions = controller(mph_file_name, False)

    pgs = []
    for id in workItem.plot_group_ids:
        pgs.append(jobs.plot_groups_catalog[id])

    # Processing the plot nodes before exporting them
    if workItem.regeneratePlots:
        generate_pgs(model,
                     pgs,
                     clearPlots=False,
                     overwritePlots=True,
                     overwriteNodes=True)

    for pg in pgs:

        # Appending to the sol count that already exists in the exports directory
        outer_sol_name_i = 0  # starting file name count

        print("\nChecking existing files for the current model name...")
        try:
            files = listdir(EXPORT_DIRECTORY)
            # print(files)
            try:
                # Separating the files that contain only the current model's name
                files = [x for x in files if model in x]
                # print("Cleaned list of files: ")
                # print(files)
                max_int = 0

                # WARNING: This is sensitive to how the folders are named.
                for file in files:
                    latter_part = str(file).split(model + " - ", 1)[1]
                    # print("latter_part:", latter_part)

                    # Find the number before the first '['
                    match = re.search(r'(\d+)', latter_part)
                    if match:
                        number = int(match.group(1))
                        if number > max_int:
                            max_int = number
                print(max_int)
                sol_name_i = max_int
            except Exception as e:
                print(e)
        except Exception as e:
            print("No export directory found.")
            sol_name_i = 0

        outer_sol_name_i += 1

        for solution in workItem.sol_elements:

            print(f"Working on - {workItem.mph_file} |"
                  f"{solution.sol} |"
                  f"{solution.view} |"
                  f"{pg} |")

            sol_title = solution.sol
            sol_node = model / 'solutions' / sol_title
            view = solution.view

            # Finding the dataset that the solution node belongs to in order to assign it
            # to the pg
            dsets = model.datasets()
            dset = ""
            name = sol_title
            # name = str(sol_node).split('/', 1)[1]
            for set in dsets:
                if name in set:
                    dset = set
            dset_node = model / 'datasets' / dset
            dset = dset_node.tag()
            # dset = get_dset_tag_for_sol(model, sol_node, datasets)
            outer_solutions = sol_node.children()

            outer_sol_i = 1

            # Iterating over the outer solutions for the current plot group
            for sol in outer_solutions:

                # Assigning the current solution to the plot node
                plot_node = model / 'plots' / pg
                export_node = model / 'exports' / pg
                plot_node.property('data', str(dset))
                plot_node.property('outersolnum', str(outer_sol_i))

                # Iterating over the qualities for the current plot group
                for q in workItem.qualities:
                    print(f"Working on - {workItem.mph_file} |"
                          f"{solution.sol} |"
                          f"{solution.view} |"
                          f"{pg} |"
                          f"quality={q}")

                    # Assigning the current quality and view to the export node
                    generate_export_node(model,
                                         True,
                                         pg_name=pg,
                                         view=view,
                                         quality=q,
                                         zoomextents=False)

                    export_2D_PG(model,
                                 pg_title=pg,
                                 export_node=export_node,
                                 sol_name=sol.name(),
                                 outer_sol_name_i=outer_sol_name_i,
                                 model_name=workItem.mph_file,
                                 quality=q,
                                 zoomextents=False)
                outer_sol_i += 1
                outer_sol_name_i += 1

            jobs_done += workItem.qualities.__len__()
            # Updating the progress bar
            progress_var.set(jobs_done)
            count_var.set(str(int(jobs_done / total_jobs * 100)) + "%")
            root.update_idletasks()
            root.update()

print("Jobs done: " + str(jobs_done) + "/" + str(total_jobs))
root.destroy()