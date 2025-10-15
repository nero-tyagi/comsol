from controllers.mphController import controller
from constants import MPH_FILES
from plotFuncs import generate_export_node, preset_plots

models, clients, datasets = controller(MPH_FILES, False)
plots = [1, 2, 3, 4, 5, 6]
view = input("What view would you like to use? 'n' for default view. ")
if view == 'n':
    view = 'view1'
for plot in plots:
    generate_export_node(models[0], False, pg_name=preset_plots.get(plot), view=view)
