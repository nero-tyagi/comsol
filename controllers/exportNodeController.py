from controllers.mphController import controller
from input_files.inputVariables import MPH_FILES
from input_files.inputVariables import EXPORT_PLOT_NODES
from constants import EXPORT_DICT
from functions.plots import generate_export_node, default_plots

models, clients, datasets = controller(MPH_FILES, False)

# Accessing plot keys from the export_plot_nodes list using the export dictionary
plots = []
for x in EXPORT_PLOT_NODES:
    for key, val in EXPORT_DICT.items():
        if val == x:
            plots.append(key)

for model in models:
    view = input("What view would you like to use? 'n' for default view. ")
    if view == 'n':
        view = 'view1'
    for plot in plots:
        generate_export_node(model, True, pg_name=default_plots.get(plot), view=view)
        # Saving the model
        model.save()