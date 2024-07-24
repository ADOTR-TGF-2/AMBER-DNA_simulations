#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:01:48 2024

@author: enp
"""

import numpy as np
import parmed as pmd

# Constants
ev_to_joules = 1.602e-19  # eV to Joules conversion factor
mass_proton_kg = 1.67e-27  # Mass of proton in kg
mass_hydrogen_kg = 1.67e-27  # Mass of hydrogen atom in kg

def calculate_impact_angle(initial_velocity_proton, initial_velocity_hydrogen):
    """
    Calculate the impact angle between the initial velocity vectors of the proton and hydrogen atom.
    """
    dot_product = np.dot(initial_velocity_proton, initial_velocity_hydrogen)
    norm_proton = np.linalg.norm(initial_velocity_proton)
    norm_hydrogen = np.linalg.norm(initial_velocity_hydrogen)
    cos_theta = dot_product / (norm_proton * norm_hydrogen)
    angle_radians = np.arccos(cos_theta)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def calculate_recoil_velocity_vector(proton_energy_ev, initial_velocity_proton, initial_velocity_hydrogen):
    """
    Calculate the recoil velocity vector of a hydrogen atom given the proton energy in eV,
    initial velocity vectors of the proton and hydrogen atom.
    """
    # Calculate the impact angle
    angle_degrees = calculate_impact_angle(initial_velocity_proton, initial_velocity_hydrogen)
    angle_radians = np.radians(angle_degrees)
    
    # Convert proton energy from eV to Joules
    proton_energy_joules = proton_energy_ev * ev_to_joules

    # Calculate proton velocity in m/s
    velocity_proton_m_per_s = np.sqrt(2 * proton_energy_joules / mass_proton_kg)
    velocity_proton_m_per_s_vector = np.array(initial_velocity_proton) * velocity_proton_m_per_s / np.linalg.norm(initial_velocity_proton)

    # Calculate recoil velocity using conservation of momentum
    velocity_recoil_m_per_s = (2 * mass_proton_kg * velocity_proton_m_per_s_vector * np.cos(angle_radians)) / (mass_proton_kg + mass_hydrogen_kg)

    # Add the initial velocity of the hydrogen atom
    initial_velocity_hydrogen_m_per_s = np.array(initial_velocity_hydrogen)
    final_velocity_hydrogen_m_per_s = initial_velocity_hydrogen_m_per_s + velocity_recoil_m_per_s

    # Convert m/s to Å/ps
    final_velocity_hydrogen_angstrom_per_ps = final_velocity_hydrogen_m_per_s * 1e-2  # 1 m/s = 10^-2 Å/ps

    return final_velocity_hydrogen_angstrom_per_ps, angle_degrees

def calculate_magnitude(vector):
    """
    Calculate the magnitude of a vector.
    """
    return np.linalg.norm(vector)

# Define paths to the input files
topology_file = 'dna_water_topology.prmtop'
restart_file = 'equilibration/dna_equilibrated.rst'

topology = pmd.load_file(topology_file)
restart = pmd.amber.Rst7.open(restart_file)

# Extract atom names
atom_names = [atom.name for atom in topology.atoms]

# Extract velocities and coordinates
velocities = restart.velocities
coordinates = restart.coordinates

# Print atom names with their velocities
print('unmodified velocities')
for i, name in enumerate(atom_names[:10]):
    print(f'Atom {i}: {name}, Velocity: {velocities[i]}')
print()

# Identify the index of the hydrogen atom you want to modify
hydrogen_indices = [i for i, name in enumerate(atom_names) if 'H' in name]

# Pick the first hydrogen atom
hydrogen_index = hydrogen_indices[0]
print(f'Modifying velocity of atom {hydrogen_index}: {atom_names[hydrogen_index]}')
print()

#initial_velocity_proton = [1.0, 0.0, 0.0]
initial_velocity_proton = [-0.457, 0.185, -0.871]  # Initial Unit velocity vector of the proton (matches the direction of the HO5' atom)
OG_initial_velocity_hydrogen = velocities[hydrogen_index].copy()  # Initial velocity vector of the hydrogen atom


output_file_path = 'modified_restart_files/velocity.out'

for proton_energy_ev in np.arange(1.0, 6.0, 1.0):
# Calculate the new recoil velocity vector for the hydrogen atom
    initial_velocity_hydrogen = np.array(OG_initial_velocity_hydrogen)
    new_velocity, impact_angle = calculate_recoil_velocity_vector(proton_energy_ev, initial_velocity_proton, initial_velocity_hydrogen)
    velocities[hydrogen_index] = new_velocity

# Calculate the magnitude of the new hydrogen velocity vector
    magnitude_new_velocity = calculate_magnitude(new_velocity)
    magnitude_old_velocity = calculate_magnitude(OG_initial_velocity_hydrogen)

# Save the new restart file with the modified velocities
    restart.vels = velocities
    restart.write(f'modified_restart_files/{atom_names[hydrogen_index]}_{proton_energy_ev:.2f}eV_{magnitude_new_velocity:.2f}Aps.rst')

# Write output to a file

    with open(output_file_path, 'a') as output_file:
        output_file.write(f'New restart file created: {atom_names[hydrogen_index]}_{proton_energy_ev:.2f}eV_{magnitude_new_velocity:.2f}Aps.rst\n')
        output_file.write(f'Modified velocity of atom {hydrogen_index}: {atom_names[hydrogen_index]},Original velocity Vector:{initial_velocity_hydrogen}, New Velocity vector: {new_velocity}\n')
        output_file.write(f'Impact angle: {impact_angle:.2f} degrees\n')
        output_file.write(f'Proton energy: {proton_energy_ev:.2f} eV\n')
        output_file.write(f'Magnitude of original hydrogen velocity vector: {magnitude_old_velocity:.2f} Å/ps\n')
        output_file.write(f'Magnitude of new hydrogen velocity vector: {magnitude_new_velocity:.2f} Å/ps\n')
        output_file.write('\n')

    print(f'New restart file created: {atom_names[hydrogen_index]}_{proton_energy_ev:.2f}eV_{magnitude_new_velocity:.2f}Aps.rst')
    print(f'Modified velocity of atom {hydrogen_index}: {atom_names[hydrogen_index]}, Original velocity Vector:{initial_velocity_hydrogen}, New Velocity vector: {velocities[hydrogen_index]}')
    print(f'Impact angle: {impact_angle:.2f} degrees')
    print(f'Proton energy: {proton_energy_ev:.2f} eV')
    print(f'Magnitude of original hydrogen velocity vector: {magnitude_old_velocity:.2f} Å/ps')
    print(f'Magnitude of new hydrogen velocity vector: {magnitude_new_velocity:.2f} Å/ps')
    print()

