#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:14:15 2024

@author: enp
"""

import parmed as pmd
import matplotlib.pyplot as plt

# Load the topology file
topology = pmd.load_file('dna_water_topology.prmtop')

# Load the restart file to get the coordinates (optional, can use trajectory file)
initial_restart = pmd.amber.Rst7.open('modified_dna_equilibrated.rst')
restart = pmd.amber.Rst7.open('modified_dna_equilibrated_QM.rst')

# Load the initial coordinates (assuming the initial coordinates are available)
initial_coordinates = initial_restart.coordinates[0]  # This is an example, adjust as necessary

# Load the trajectory file
trajectory = pmd.load_file('modified_dna_equilibrated_QM.nc')

# Extract coordinates from the final configuration
coordinates = restart.coordinates[0]

# Assign coordinates to the topology object
topology.coordinates = coordinates

# Function to calculate the distance between two atoms
def calculate_distance(atom1, atom2, coordinates):
    x1, y1, z1 = coordinates[atom1.idx]
    x2, y2, z2 = coordinates[atom2.idx]
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5

# Analyze all bonds in the final configuration
bond_distances_final = []
for bond in topology.bonds:
    atom1 = bond.atom1
    atom2 = bond.atom2
    distance = calculate_distance(atom1, atom2, coordinates)
    bond_distances_final.append((atom1, atom2, distance))

# Analyze all bonds in the initial configuration
bond_distances_initial = []
for bond in topology.bonds:
    atom1 = bond.atom1
    atom2 = bond.atom2
    distance = calculate_distance(atom1, atom2, initial_coordinates)
    bond_distances_initial.append((atom1, atom2, distance))

# Filter DNA bonds
def is_dna_atom(atom):
    return 'D' in atom.residue.name  # Assuming DNA residues have names like DA, DC, DG, DT

dna_bond_distances_final = [bond for bond in bond_distances_final if is_dna_atom(bond[0]) or is_dna_atom(bond[1])]
dna_bond_distances_initial = [bond for bond in bond_distances_initial if is_dna_atom(bond[0]) or is_dna_atom(bond[1])]

target_atom_index = 0
# Analyze specific target bonds in final configuration
hydrogen_bond_distances_final = []
for bond in topology.bonds:
    atom1 = bond.atom1
    atom2 = bond.atom2
    if target_atom_index in [atom1.idx, atom2.idx]:
        distance = calculate_distance(atom1, atom2, coordinates)
        hydrogen_bond_distances_final.append((atom1, atom2, distance))

# Analyze bond distances involving specific hydrogen over multiple frames
hydrogen_bond_distances = []
for frame_index, frame in enumerate(trajectory.coordinates):
    for bond in topology.bonds:
        atom1 = bond.atom1
        atom2 = bond.atom2
        if target_atom_index in [atom1.idx, atom2.idx]:
            distance = calculate_distance(atom1, atom2, frame)
            hydrogen_bond_distances.append((frame_index, atom1, atom2, distance))

def print_bond_info(option):
    if option == 1:
        # Print all bond distances
        print("First 10 Bond Distances (all bonds):")
        for bond in bond_distances_final[:10]:
            atom1, atom2, distance = bond
            print(f'Bond between {atom1.name} ({atom1.idx}) and {atom2.name} ({atom2.idx}) has a length of {distance:.2f} Angstroms')
    elif option == 2:
        # Print only the first 10 hydrogen bond distances
        print("First 10 Hydrogen Bond Distances (specific bonds):")
        for bond in hydrogen_bond_distances_final[:10]:
            atom1, atom2, distance = bond
            print(f'Bond between {atom1.name} ({atom1.idx}) and {atom2.name} ({atom2.idx}) has a length of {distance:.2f} Angstroms')
    elif option == 3:
        # Print the distances for 'HO5' bonds over all frames
        print("Hydrogen Bond Distances Over All Frames:")
        for frame_index, atom1, atom2, distance in hydrogen_bond_distances[:20]:  # Print only first 20 entries
            print(f'Frame {frame_index}: Bond between {atom1.name} ({atom1.idx}) and {atom2.name} ({atom2.idx}): Bond distance {distance:.2f} Angstroms')
    else:
        print("Invalid option. Please select 1, 2, or 3.")

def plot_bond_distances(option):
    if option == 1:
        # Plot hydrogen bond distances over frames
        frames = [entry[0] for entry in hydrogen_bond_distances]
        distances = [entry[3] for entry in hydrogen_bond_distances]
        atom1_name = hydrogen_bond_distances[0][1].name
        atom2_name = hydrogen_bond_distances[0][2].name

        plt.figure(figsize=(10, 6))
        plt.plot(frames, distances, marker='o', linestyle='-')
        plt.xlabel('Frame Index')
        plt.ylabel('Bond Distance (Angstroms)')
        plt.title(f'Bond Distances for {atom1_name} and {atom2_name} over Frames')
        plt.grid(True)
        plt.show()
    elif option == 2:
        # Plot DNA bond distances in the initial and final configurations
        atom1_names = [bond[0].name for bond in dna_bond_distances_final]
        atom2_names = [bond[1].name for bond in dna_bond_distances_final]
        distances_final = [bond[2] for bond in dna_bond_distances_final]
        distances_initial = [bond[2] for bond in dna_bond_distances_initial]

        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(distances_final)), distances_final, marker='o', label='Final Configuration')
        plt.scatter(range(len(distances_initial)), distances_initial, marker='x', label='Initial Configuration')
        plt.xlabel('Bond Index')
        plt.ylabel('Bond Distance (Angstroms)')
        plt.title('DNA Bond Distances in Initial and Final Configurations')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Invalid option. Please select 1 or 2.")

# Example usage
print_bond_info(1)  # This will print all bond distances
#print_bond_info(2)  # This will print the final (restart file) bond distance
#print_bond_info(3)  # This will print the distances for over all frames

# Plot the bond distances
plot_bond_distances(1)  # Plot hydrogen bond distances over frames
plot_bond_distances(2)  # Plot DNA bond distances in initial and final configurations
