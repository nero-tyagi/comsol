from controllers.mphController import controller
from input_files.inputVariables import MPH_FILES

models, clients, datasets = controller(MPH_FILES, False)
model = models[0]

dsets = model.datasets()
tags = []
dset_collec = []
for dset in dsets:
    node = model / 'datasets' / dset
    tags.append(node.tag())

for ix, x in enumerate(dsets):
    dset_collec.append([dsets[ix], tags[ix]])
print("Datasets")
print(dset_collec)
print()

node = model / 'solutions'
print("Solutions children")
print(node.children())
print()

node = model / 'plots' / 'Continuous Phase Velocity'
print("Uc properties")
print(node.properties())
print()