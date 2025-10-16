from functions.mph import *

# Check the values returned by any get function
def check_get_function(func, *args):
    print("Checking the function " + func.__name__ + ". Output:")
    print(str(func(*args)))

# Prints the geometries, meshes, parameters, physics, studies, and results contained
# in the model
def print_model_details(model, client):
    print(get_client_names(client))
    parameters = get_parameters(model)
    print(parameters)
    print('Physics modules available in this model: ' + str(get_physics(model)))

# Prints all the parameters present inside the model in a clear list
def print_parameters(model):
    for (name, value) in model.parameters().items():
        description = model.description(name)
        print(f'{description:20} {name} = {value}')

# Prints the current node's name, parent's name, and its children's names
def print_node_details(node, model):
    print('Node details:\n\nName: '+ str(node.name()) + '\nParent: '
          + str(node.parent()) + '\nChildren: ' + str(node.children()) +
          '\nProperties:')
    properties = model.properties(node)
    if properties is not []:
        for name, value in properties.items():
            print('\t' + name + ': ' + str(value))
    else:
        print('\tNo properties')
    print('\n\n')
