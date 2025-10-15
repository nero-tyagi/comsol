import mph

# Returns the names of all the clients open in memory
def get_client_names(client):
    return client.names()

# Returns a 2-D array of all the parameters inside a model. The first element represents
# the name of the parameter and the second element represents the value.
def get_parameters(model):
    parameters = []
    for (name, value) in model.parameters().items():
        parameter = [name, value]
        parameters.append(parameter)


# Returns the value of a stated parameter
def get_parameter(model, parameter_name):
    return model.parameter(parameter_name)

# Returns all the physics modules present inside the model
def get_physics(model):
    return model.physics()

# Returns all the materials present inside the model
def get_materials(model):
    return model.materials()

# Returns all the meshes present inside the model
def get_meshes(model):
    return model.meshes()

# Returns all the studies present inside the model
def get_studies(model):
    return model.studies()

# Returns all the solutions present inside the model
def get_solutions(model):
    return model.solutions()

# Returns all the solutions present inside the model
def get_datasets(model):
    return model.solutions()

# Returns all the solutions present inside the model
def get_plots(model):
    return model.plots()

# Returns all the solutions present inside the model
def get_exports(model):
    return model.exports()

# Returns all the solutions present inside the model
def get_problems(model):
    return model.problems()

def get_node_properties(node):
    node_properties = []
    node_properties_readable = ""
    for i in node.properties():
        property = []
        property.append(i)
        property.append(node.property(i))
        property.append(type(node.property(i)))
        node_properties_readable += i
        node_properties_readable += (" = " + str(node.property(i)) +
                            "[" + str(type(node.property(i))) + "]")
        node_properties_readable += "\n"
        node_properties.append(property)
    return node_properties, node_properties_readable

def clearPlotGroups(model):
    pg_nodes = model/'plots'
    for node in pg_nodes:
        node.remove()

def clearExportNodes(model):
    export_nodes = model/'exports'
    for node in export_nodes:
        node.remove()