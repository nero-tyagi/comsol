import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import ezdxf

matplotlib.rcParams.update({'text.usetex': True})

filenames = ["front", "middle", "rear", "outlet"]
Sts = [0.001, 0.01, 0.1, 1, 2]
# Sts = [0.005, 0.01, 0.015, 0.02, 0.025]

def plot_same_stokes(model):
    global filenames

    sol_node = model / 'solutions' / 'Parametric Solutions 1'
    outer_solutions = sol_node.children()

    for file in filenames:
        directory = "Exports/line-plots" + "/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory = directory + file + "/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        column_names = ['r', 'z']
        for outer_solution in outer_solutions:
            column_names.append(str(outer_solution.name()))

        line_data = pd.read_table(file + ".txt", delimiter='\t', names=column_names)

        i = 0
        for St in Sts:
            print("Stokes number = " + str(St))
            plot_data = []

            figure = plt.figure(figsize=(6, 6), dpi=400)
            plt.xlabel(r'$\phi$', fontsize=22)
            plt.ylabel('Z (cm)', fontsize=22)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)


            for j in range(i, 15, 5):
                solution_name = clean_variable_name(outer_solutions[j].name())
                print("Using solution: " + str(solution_name))
                if file == 'outlet':
                    plot_data.append({
                        'x': np.array(line_data['r']),
                        'y': np.array(line_data[str(outer_solutions[j].name())]),
                        'label': solution_name
                    })
                else:
                    plot_data.append({
                        'x': np.array(line_data[str(outer_solutions[j].name())]),
                        'y': np.array(line_data['z']),
                        'label': solution_name
                    })

            phiMax = 0
            phiMin = 1
            phiRange = 0
            phiMidpoint = 0

            if file == 'outlet':
                for data in plot_data:
                    if max(data['y']) > phiMax:
                        phiMax = max(data['y'])
                    if min(data['y']) < phiMin:
                        phiMin = min(data['y'])
                phiRange = abs(phiMax - phiMin)
                phiMidpoint = (phiMin + phiMax) / 2
            else:
                for data in plot_data:
                    if max(data['x']) > phiMax:
                        phiMax = max(data['x'])
                    if min(data['x']) < phiMin:
                        phiMin = min(data['x'])
                phiRange = abs(phiMax - phiMin)
                phiMidpoint = (phiMin + phiMax) / 2

            for data in plot_data:
                plt.plot(data['x'], data['y'], label=data['label'])
            if file == 'outlet':
                plt.ylim(phiMidpoint - phiRange, phiMidpoint + phiRange)
                plt.ylabel('r (cm)', fontsize=22)
            else:
                plt.xlim(phiMidpoint - phiRange, phiMidpoint + phiRange)
                plt.ylabel('z (cm)', fontsize=22)

            plt.legend(bbox_to_anchor=(0, 1.04), loc="lower left", fontsize=18)
            plt.tight_layout()
            plt.grid(True, alpha=0.3)
            plt.minorticks_on()
            plt.grid(True, which='minor', alpha=0.15)
            # figure.show()
            figure.savefig(directory + "St = " + f"{St:.3f}" + ".png")
            print(str(St) + ".png saved.")
            plt.clf()
            plt.close(figure)

            i += 1

def plot_stokes_eval(model):
    global filenames

    sol_node = model / 'solutions' / 'Parametric Solutions 1'
    outer_solutions = sol_node.children()

    stokes0005 = []
    stokes0025 = []
    r = []

    for file in filenames:
        directory = "Exports"
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory = "Exports/line-plots/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory = directory + "stokes-eval/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        column_names = ['r', 'z']
        for outer_solution in outer_solutions:
            column_names.append(str(outer_solution.name()))

        line_data = pd.read_table(file + ".txt", delimiter='\t', names=column_names)

        figure = plt.figure(figsize=(9, 6), dpi=400)
        plt.xlabel(r'$\phi$', fontsize=22)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        phiMax = 0
        phiMin = 100
        phiRange = 0
        phiMidpoint = 0

        i = 0
        for St in Sts:
            print("Stokes number = " + str(St))

            same_stokes_phi_values = np.zeros(shape=(len(line_data[str(outer_solutions[0].name())])))
            for j in range(i, 15, 5):
                for k in range(len(line_data[str(outer_solutions[j].name())])):
                    same_stokes_phi_values[k] += (line_data[str(outer_solutions[j].name())][k])
            for j in range(0, len(same_stokes_phi_values), 1):
                same_stokes_phi_values[j] = same_stokes_phi_values[j] / 3

            if St == Sts[0]:
                if file == 'outlet':
                    print("st 0005 and file    ")
                    stokes0005 = same_stokes_phi_values
                    r = line_data['r']
            elif St == Sts[-1]:
                if file == 'outlet':
                    print("st 0025 and file outlet")
                    stokes0025 = same_stokes_phi_values

            phiMax = max(same_stokes_phi_values)
            phiMin = min(same_stokes_phi_values)
            phiRange = abs(phiMax - phiMin)
            phiMidpoint = (phiMin + phiMax) / 2

            if file == 'outlet':
                plt.plot(line_data['r'], same_stokes_phi_values, label=St)
                plt.ylabel('r (cm)', fontsize=22)
            else:
                plt.plot(same_stokes_phi_values, line_data['z'], label=St)
                plt.ylabel('z (cm)', fontsize=22)
            i += 1

        # if file == 'outlet':
        #     plt.ylim(phiMidpoint - phiRange, phiMidpoint + phiRange)
        # else:
        #     plt.xlim(phiMidpoint - phiRange, phiMidpoint + phiRange)
        plt.legend(bbox_to_anchor=(0.04, 1), loc="upper left", fontsize=18)
        plt.tight_layout()
        plt.grid(True, alpha=0.3)
        plt.minorticks_on()
        plt.grid(True, which='minor', alpha=0.15)
        figure.savefig(directory + "stokes-eval-" + file + ".png")
        print(directory + "stokes-eval-" + file + ".png saved.")
        plt.clf()
        plt.close(figure)

    # Outlet max and min Stokes eval:
    diff = np.array(stokes0025) - np.array(stokes0005)
    phiMax = max(diff)
    phiMin = min(diff)
    phiRange = abs(phiMax - phiMin)
    phiMidpoint = (phiMin + phiMax) / 2

    figure = plt.figure(figsize=(6, 6), dpi=300)
    ax = figure.add_subplot(111)

    ax.set_xlabel('r (cm)', fontsize=22)
    plt.tight_layout()
    plt.subplots_adjust(left=0.2)
    ax.set_ylabel(r'$\phi_{0.025} - \phi_{0.005}$', fontsize=22)
    ax.tick_params(axis='both', labelsize=18)
    ax.set_ylim(phiMidpoint - phiRange, phiMidpoint + phiRange)
    ax.grid(True, alpha=0.3)
    ax.minorticks_on()
    ax.grid(True, which='minor', alpha=0.15)
    ax.plot(r, diff)

    print("Saving - Exports/line-plots/stokes-eval/min-max-outlet.png")
    figure.savefig("Exports/line-plots/stokes-eval/min-max-outlet.png")

def clean_variable_name(name):

    variable_names = {
        'dd': 'D_d',
        'rho_d': r'\rho_d'
    }

    cleaned = name.replace(" ", "")
    expressions = cleaned.split(",")
    parts = []
    result = r'$'
    for expression in expressions:
        for subpart in expression.split("="):
            parts.append(subpart)
    for part in parts:
        if part in variable_names:
            result += (variable_names.get(part))
            result += " = "
        else:
            result += (part)
            result += ", "
    result = result[:-2]
    result += "$"

    print(result)
    return result
