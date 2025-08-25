from mphFunctions import *
import os

# Test whether the mph module is working
def mph_test():
    client = mph.start()
    model = client.create('empty')
    model.save()

# Clear the loaded clients from memory
def clear_clients(client):
    client.clear()

# Import an MPh file
def mph_import(file, file_name):

    if os.path.exists(file):
        print("Loading mph file: " + file + "\n")
        # Checking if the client already exists in memory.
        already_loaded = False
        client = mph.start()
        client_names = get_client_names(client)
        print('Active clients: ' + str(client_names))

        for name in client_names:
            if name == file_name:
                already_loaded = True
                print('This client has already been loaded!')
                break
        if not already_loaded:
            print('The requested model is not currently loaded. Loading the model'
                  ' from disk.')
            model = client.load(file)
        else:
            # If multiple clients are loaded, accessing the last client loaded.
            model = client.models()[-1]
        return model, client
    else:
        print("The mph file was not found.")
    return None

# Checking the directory for available files and then loading it using the MPh library.
# If the function can't find the input files, please check the directory and filenames in
# main.py. Also, confirm that the file you hope to import has the extension ".mph".

def mph_import_controller(files, display_node_tree = False):
    mphLoadedCorrectly = False
    models = []
    clients = []
    for file in files:

        print(file)
        file_name = os.path.basename(file)

        # Importing the mph file
        model, client = mph_import(file, file_name)
        models.append(model)
        clients.append(clients)

        # Checking if the client could be loaded properly
        if client is not None and model is not None:
            mphLoadedCorrectly = True
        elif client is None:
            print("Client couldn't be loaded")
        elif model is None:
            print("Model couldn't be loaded")

        if mphLoadedCorrectly:
            datasets = get_datasets(model)
            print("\nDatasets available: ")
            for set in datasets:
                print(str(set))
            print()
            if display_node_tree:
                model_tree = mph.tree(model)

            model.save()
        mphLoadedCorrectly = False
    return models, clients