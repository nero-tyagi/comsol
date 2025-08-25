from getFunctions import *
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
def mph_import(address, current_file_name):

    # Checking if the client already exists in memory.
    already_loaded = False
    client = mph.start()
    client_names = get_client_names(client)
    print('Active clients: ' + str(client_names))

    for name in client_names:
        if name == current_file_name:
            already_loaded = True
            print('This client has already been loaded!')
            break
    if not already_loaded:
        print('The requested model is not currently loaded. Loading the model'
              ' from disk.')
        model = client.load(address)
    else:
        # If multiple clients are loaded, accessing the last client loaded.
        model = client.models()[-1]
    return model, client

# Checking the directory for available files and then loading it using the MPh library.
# If the function can't find the input files, please check the directory and filenames in
# main.py. Also, confirm that the file you hope to import has the extension ".mph".

def mph_import_controller(directory_path, file_name):

    file_path = directory_path + file_name + ".mph"
    print(file_path)
    if os.path.exists(file_path):
        print("Loading mph file: " + file_path + "\n")
        model, client = mph_import(file_path, file_name)
        return model, client
    else:
        print("The mph file is not found.")
    return None