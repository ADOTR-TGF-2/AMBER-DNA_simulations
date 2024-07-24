#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:17:21 2024

@author: enp
"""

import parmed as pmd

restart_modified = pmd.amber.Rst7.open('modified_dna_equilibrated.rst')
topology_file = 'dna_water_topology.prmtop'
topology = pmd.load_file(topology_file)

# Extract atom names
atom_names = [atom.name for atom in topology.atoms]

velocities_modified = restart_modified.velocities
# Print atom names with their velocities
for i, name in enumerate(atom_names[:10]):
    print(f'Atom {i}: {name}, Velocity: {velocities_modified[i]}')