from mphController import mph_import_controller
from constants import MPH_FILES
from plotFuncs import generate_default_pgs

# Run this file using a Pycharm configuration to generate all the default plots.
#WARNING: The following code overwrites the default plots.

models, clients = mph_import_controller(MPH_FILES, False)
generate_default_pgs(models, overwritePlots=True)