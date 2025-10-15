# from newPlot import generate_default_pgs
# from exportFunctions import batch_export_Uc_plots
from generatePresets import genProps
from controllers.mphController import controller
from constants import MPH_FILES, PRESETS_FOLDER
from mphFunctions import get_node_properties
from plotFuncs import generate_export_node, preset_plots

# generate_default_pgs(models, True, True)

models, clients, datasets = controller(MPH_FILES, False)
models[0].export(models[0]/'exports'/'Continuous Phase Velocity', file="Exports/Uc")