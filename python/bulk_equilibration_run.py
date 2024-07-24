#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:56:02 2024

@author: enp
"""

import subprocess
import parmed as pmd
import os

# List of file names
'''
file_names = [
    "HO5_0.01eV_14.15Aps", "HO5_0.14eV_52.12Aps", "HO5_0.27eV_72.27Aps", "HO5_0.40eV_87.90Aps",
    "HO5_0.02eV_19.89Aps", "HO5_0.15eV_53.94Aps", "HO5_0.28eV_73.59Aps", "HO5_0.41eV_88.99Aps",
    "HO5_0.03eV_24.29Aps", "HO5_0.16eV_55.70Aps", "HO5_0.29eV_74.89Aps", "HO5_0.42eV_90.06Aps",
    "HO5_0.04eV_28.00Aps", "HO5_0.17eV_57.41Aps", "HO5_0.30eV_76.16Aps", "HO5_0.43eV_91.13Aps",
    "HO5_0.05eV_31.27Aps", "HO5_0.18eV_59.06Aps", "HO5_0.31eV_77.42Aps", "HO5_0.44eV_92.18Aps",
    "HO5_0.06eV_34.23Aps", "HO5_0.19eV_60.67Aps", "HO5_0.32eV_78.65Aps", "HO5_0.45eV_93.21Aps",
    "HO5_0.07eV_36.94Aps", "HO5_0.20eV_62.24Aps", "HO5_0.33eV_79.87Aps", "HO5_0.46eV_94.24Aps",
    "HO5_0.08eV_39.47Aps", "HO5_0.21eV_63.77Aps", "HO5_0.34eV_81.06Aps", "HO5_0.47eV_95.26Aps",
    "HO5_0.09eV_41.85Aps", "HO5_0.22eV_65.27Aps", "HO5_0.35eV_82.24Aps", "HO5_0.48eV_96.26Aps",
    "HO5_0.10eV_44.10Aps", "HO5_0.23eV_66.73Aps", "HO5_0.36eV_83.40Aps", "HO5_0.49eV_97.26Aps",
    "HO5_0.11eV_46.24Aps", "HO5_0.24eV_68.15Aps", "HO5_0.37eV_84.55Aps", "HO5_0.50eV_98.24Aps",
    "HO5_0.12eV_48.28Aps", "HO5_0.25eV_69.55Aps", "HO5_0.38eV_85.68Aps",
    "HO5_0.13eV_50.24Aps", "HO5_0.26eV_70.93Aps", "HO5_0.39eV_86.80Aps"
]

file_names = [
    "HO5_0.01eV_14.15Aps",
    "HO5_0.05eV_31.27Aps", 
    "HO5_0.10eV_44.10Aps",
    "HO5_0.15eV_53.94Aps", 
    "HO5_0.20eV_62.24Aps",
    "HO5_0.25eV_69.55Aps",
    "HO5_0.30eV_76.16Aps", 
    "HO5_0.35eV_82.24Aps", 
    "HO5_0.40eV_87.90Aps",
    "HO5_0.45eV_93.21Aps",
    "HO5_0.50eV_98.24Aps" 
]
'''

file_names = [
    "HO5_1.00eV_138.81Aps",
    "HO5_2.00eV_196.18Aps",
    "HO5_3.00eV_240.21Aps",
    "HO5_4.00eV_277.32Aps",
    "HO5_5.00eV_310.02Aps"

]

# Full path to the AMBER executable
amber_executable = '/home/enp/amber/amber22/bin/sander'  # Adjust the path as needed

# Define paths to the input files
topology_file = 'dna_water_topology.prmtop'
input_file = 'equil_QM.in'

for filename in file_names:
    initial_coordinates = 'modified_restart_files/' + filename + '.rst'
    output_file = filename + '_QM.out'
    final_restart_file = filename + '_QM.rst'
    trajectory_file = filename + '_QM.nc'
    info_file = filename + '_QM.info'
    reference_file = initial_coordinates
    output_pdb = filename + '_QM.pdb'

    # Construct the full command to run the equilibration
    command = f"{amber_executable} -O -i {input_file} -o {output_file} -p {topology_file} -c {initial_coordinates} -r {final_restart_file} -x {trajectory_file} -inf {info_file} -ref {reference_file}"

    # Run the equilibration using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        print(f'Equilibration run completed successfully. Output written to {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred during equilibration run: {e}')

    def convert_nc_to_pdb(topology_file, trajectory_file, output_pdb):
        """
        Convert a NetCDF file with modified velocities to a PDB file readable in OVITO.

        Parameters:Python
        topology_file (str): Path to the topology file (.prmtop).
        nc_file (str): Path to the NetCDF file (.nc).
        output_pdb (str): Path to the output PDB file (.pdb).
        """
        # Load the topology and NetCDF file
        parm = pmd.load_file(topology_file, trajectory_file)

        # Write out to PDB
        parm.save(output_pdb, format='pdb', overwrite=True)
        print(f'Converted NetCDF to PDB: {output_pdb}')

    convert_nc_to_pdb(topology_file, trajectory_file, output_pdb)
