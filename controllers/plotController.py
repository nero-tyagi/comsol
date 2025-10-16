from controllers.mphController import controller
from constants import MPH_FILES
from functions.plots import generate_default_pgs

# Run this file using a Pycharm configuration to generate all the default plots.
#WARNING: The following code overwrites the default plots.

models, clients, datasets = controller(MPH_FILES, False)
generate_default_pgs(models, overwritePlots=True)