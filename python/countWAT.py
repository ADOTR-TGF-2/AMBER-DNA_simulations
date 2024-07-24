from ovito.io import import_file
from ovito.data import *
from ovito.modifiers import *

# Load the PDB file
pipeline = import_file('/home/enp/amber/amber22/DNA_simulations/Shepard_et_al/dna_solvated.pdb')

# Define a modifier function to count water molecules
def count_water_molecules(frame, data):
    # Get the particle property containing the atom names
    atom_names = data.particles['Particle Type']

    # Initialize a counter for oxygen atoms (part of water molecules)
    oxygen_count = 0

    # Assuming 'O' corresponds to oxygen atoms in water
    for atom in atom_names:
        if atom == 'O':
            oxygen_count += 1

    # Number of water molecules is the number of oxygen atoms divided by 1 (since each water has one oxygen atom)
    water_molecule_count = oxygen_count

    # Output the number of water molecules
    print(f"Number of water molecules: {water_molecule_count}")

# Insert the modifier into the pipeline
pipeline.modifiers.append(PythonScriptModifier(function=count_water_molecules))

# Compute the pipeline to trigger the modifier
pipeline.compute()
