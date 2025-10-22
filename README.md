# COMSOL Processing

## Introduction
Hello! This code helps you process COMSOL files. You might use COMSOL to conduct studies and
then export plots from those studies. You might even have parametric studies in your COMSOL
files that have many parameters, and exporting multiple plots for each of those parameters
and then organizing them is a pain. This code streamlines your workflow by generating
presets for all your plots and then exporting them in a standardized way.

This has only been tested for Fluids plots, but it should work for other physics plots as well.
The main kind of plotgroup that this code can handle is a 2DPlotGroup. Other plotgroups are 
experimental. Under the 2DPlotGroup category, currently supported subplots include:

- Surface Plot
- Arrow Surface Plot
- Streamlines

Other plots may be added in the future.

## Prerequisites

You need to have Python 3.8 or higher installed. The code has only been tested for COMSOL 
6.2 and 6.3. Other COMSOL versions are experimental. Use the requirements.txt file to install the
necessary packages by going into your Python environment and running the following command:

```
pip install --upgrade pip
pip install -r requirements.txt
```

Make sure that "pip" isn't aliased in your system to somewhere else.

If you use an M-series Mac system, the first time you run any of the configurations, you will get
an error saying "couldn't find a COMSOL installation". That's because the current "mph" package
has a tiny error in its `discovery.py` file. Navigate to it and search for "maci64" and replace
it with "macarm64".

## How to use this code
Once you create all the plots and edit them however you like in a COMSOL file, you can use that
file to generate presets of those plots for all your future files. Add the name(s) of the COMSOL
files in the `input_files/inputVariables.py` file. Inset your COMSOL file(s) in the `input_files`
directory. New preset files are exported in the `new_plot_presets` folder. This folder contains
directories for each plotgroup that you have in the COMSOL file, and each directory contains a
file for each plot in that plotgroup. The parent directory also contains a file for each plotgroup.

The functions that generate and read presets are present in the `functions/presets.py`file. A
PyCharm configuration to generate the presets will be included in the future. Currently, only
multiphysics physics related plot presets exist. These presets are present in the `presets_files`
directory. Once you generate your custom presets, you need to move them from the `new_plot_presets`
directory to the `presets_files` directory.

> The reason these directories exist separately is so you can make changes to the presets files
> after exporting them if need be.

Once your custom presets are ready, you can use the `Generate plots` configuration. This
will generate the default plots which are listed in the `constants.py` file, or a set of plots
of your own choosing.

When you generate plots using the aforementioned configuration, associated export nodes are also
generated. These export nodes use the default view available in the COMSOL file with 1x quality
settings. 1x = 1000 * 1000 px, png, font size = 20 pts, resolution = 96 pts. All other quality
settings are mentioned below:

1. 0.5x = 500 * 500 px, font size = 10 pts, resolution = 96 pts.
2. 2x = 2000 * 2000 px, font size = 40 pts, resolution = 96 pts.
3. 4x = 4000 * 4000 px, font size = 80 pts, resolution = 96 pts.

However, you might want the plots to export a specific view with other than default quality settings.
When you use the `Export plots` configuration, you can specify the view that you want to export
the plots from. However, if for a particular reason, you want to create export nodes that reflect
a different view or quality settings, you may do so using the `Generate export nodes` configuration.

Once you have generated the default plots and export nodes, you can use the `Export plots`
configuration. This will open the COMSOL file and prompt you to enter the following values:

1. solution node to use,
2. prefix (this would be the nomenclature of your MPh solution),
3. whether to overwrite the existing export files (say "n" if you want to continue the 
solution count from the last existing solution).
4. view to export the plots from,
5. quality settings to export the plots with,
6. whether to export additional plots with zoomextents enabled (the zoomextent property spans the view 
to contain the entire domain.)

The code will then create directories inside the 'input_files/exports' directory for each
solution (if the solution node you choose is a parametric solution). The naming scheme for the
directories is:

> Prefix *+* "-" + Solution Count + [Variable name(s)] / Quality /

### Summary

1. Create plots in COMSOL and change the settings however you like.
2. Export presets for all your plots. (to be added soon. Currently, you can only use the existing
presets)
3. Generate default plots.
4. Generate export nodes. (if you want custom view and quality settings)
5. Export all plots.

## Organization of the code

The code is organized in the following directories:

- `controllers`
: Contains the main functions that are called by the configurations.

- `functions`
: Contains the functions that are used by the controllers. The functions perform
various tasks such as reading and writing files, generating presets, and generating plots.

- `input_files`
: Contains the input files that are used by the controllers. Edit `inputVariables.py`
to change the input files.

- 'new_plot_presets'
: Contains the new presets that are generated by the controllers (to be added soon)..

- 'presets_files'
: Contains the presets that are used by the `Generate default plots` configuration.
Edit the "presets" files carefully to change the presets. It is recommended to make these changes
within the COMSOL file and export those presets instead of changing them manually if you aren't
confident in what the property variables and values are.

- 'constants.py'
: Contains the constants that are used by many of the functions and controllers. Do NOT change
unless you know what you are doing.

## Final thoughts
Using this code will help you streamline your workflow and avoid unnecessary repetitions. You might
have a certain set of plots in mind and a certain way to present them that you reuse all the time.
You can use this code to generate those plots using your custom settings and export them in a
standardized way.

This code is still in development. I will be adding more features and configurations in the future.
