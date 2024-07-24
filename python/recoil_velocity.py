#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:33:52 2024

@author: enp
"""

import numpy as np

def calculate_recoil_velocity(proton_energy_ev, angle_degrees):
    # Constants
    ev_to_joules = 1.602e-19  # eV to Joules conversion factor
    mass_hydrogen_kg = 1.67e-27  # Mass of hydrogen atom in kg
    mass_proton_kg = 1.67e-27  # Mass of proton in kg

    # Convert proton energy from eV to Joules
    proton_energy_joules = proton_energy_ev * ev_to_joules

    # Calculate proton velocity in m/s
    velocity_proton_m_per_s = np.sqrt(2 * proton_energy_joules / mass_proton_kg)

    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate recoil velocity using conservation of momentum
    velocity_recoil_m_per_s = (2 * mass_proton_kg * velocity_proton_m_per_s * np.cos(angle_radians)) / (mass_proton_kg + mass_hydrogen_kg)

    # Convert m/s to Å/ps
    velocity_recoil_angstrom_per_ps = velocity_recoil_m_per_s * 1e-2  # 1 m/s = 10^-2 Å/ps

    return velocity_recoil_angstrom_per_ps

def calculate_proton_energy(recoil_velocity_angstrom_per_ps, angle_degrees):
    # Constants
    ev_to_joules = 1.602e-19  # eV to Joules conversion factor
    mass_hydrogen_kg = 1.67e-27  # Mass of hydrogen atom in kg
    mass_proton_kg = 1.67e-27  # Mass of proton in kg

    # Convert recoil velocity from Å/ps to m/s
    velocity_recoil_m_per_s = recoil_velocity_angstrom_per_ps * 1e2  # 1 Å/ps = 10^2 m/s

    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate proton velocity in m/s using inverse of momentum conservation formula
    velocity_proton_m_per_s = (velocity_recoil_m_per_s * (mass_proton_kg + mass_hydrogen_kg)) / (2 * mass_proton_kg * np.cos(angle_radians))

    # Calculate proton energy in Joules
    proton_energy_joules = 0.5 * mass_proton_kg * velocity_proton_m_per_s**2

    # Convert proton energy from Joules to eV
    proton_energy_ev = proton_energy_joules / ev_to_joules

    return proton_energy_ev

# Example usage
proton_energy_ev = 2
angle_degrees = 0
recoil_velocity = calculate_recoil_velocity(proton_energy_ev, angle_degrees)
print(f'Recoil velocity for a {proton_energy_ev} eV proton at {angle_degrees} degrees: {recoil_velocity:.2f} Å/ps')

recoil_velocity_input = 100  # recoil velocity in Å/ps
calculated_proton_energy = calculate_proton_energy(recoil_velocity_input, angle_degrees)
print(f'Proton energy for a recoil velocity of {recoil_velocity_input:.2f} Å/ps at {angle_degrees} degrees: {calculated_proton_energy:.2f} eV')
