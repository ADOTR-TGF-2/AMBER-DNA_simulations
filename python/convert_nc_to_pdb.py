#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:43:20 2024

@author: enp
"""

import parmed as pmd

def convert_nc_to_pdb(topology_file, nc_file, output_pdb):
    """
    Convert a NetCDF file with modified velocities to a PDB file readable in OVITO.

    Parameters:
    topology_file (str): Path to the topology file (.prmtop).
    nc_file (str): Path to the NetCDF file (.nc).
    output_pdb (str): Path to the output PDB file (.pdb).
    """
    # Load the topology and NetCDF file
    parm = pmd.load_file(topology_file, nc_file)

    # Write out to PDB
    parm.save(output_pdb, format='pdb', overwrite=True)
    print(f'Converted NetCDF to PDB: {output_pdb}')

# Example usage
topology_file = '../Garrec_et_al/dna_bsc1.prmtop'
nc_file = '../Garrec_et_al/QM_unmodified.nc'
output_pdb = '../Garrec_et_al/QM_unmodified.pdb'

convert_nc_to_pdb(topology_file, nc_file, output_pdb)
