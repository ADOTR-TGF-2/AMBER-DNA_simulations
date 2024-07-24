#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:57:12 2024

@author: enp
"""

import subprocess
import parmed as pmd
import os

# Define paths to the input files
filename = 'dna_equilibrated'
topology_file = 'dna_water_topology.prmtop'
initial_coordinates = 'equilibration/'+filename+'.rst'
input_file = 'equil_QM.in'
output_file = filename+'_QM.out'
final_restart_file = filename+'_QM.rst'
trajectory_file = filename+'_QM.nc'
info_file = filename+'_QM.info'
reference_file = initial_coordinates
output_pdb = filename+'_QM.pdb'

# Full path to the AMBER executable
amber_executable = '/home/enp/amber/amber22/bin/sander'  # Adjust the path as needed
    
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
