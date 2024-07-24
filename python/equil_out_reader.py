#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 17:48:54 2024

@author: enp
"""

import re
import matplotlib.pyplot as plt

def read_equil_out(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nstep_values = []
    etot_values = []
    ektot_values = []
    temp_values = []

    nstep_pattern = re.compile(r'NSTEP\s+=\s+(\d+)')
    temp_pattern = re.compile(r'TEMP\(K\)\s+=\s+([-+]?[0-9]*\.?[0-9]+)')
    etot_pattern = re.compile(r'Etot\s+=\s+([-+]?[0-9]*\.?[0-9]+)')
    ektot_pattern = re.compile(r'EKtot\s+=\s+([-+]?[0-9]*\.?[0-9]+)')

    for line in lines:
        nstep_match = nstep_pattern.search(line)
        temp_match = temp_pattern.search(line)
        etot_match = etot_pattern.search(line)
        ektot_match = ektot_pattern.search(line)

        if nstep_match:
            nstep_values.append(int(nstep_match.group(1)))
        if temp_match:
            temp_values.append(float(temp_match.group(1)))
        if etot_match:
            etot_values.append(float(etot_match.group(1)))
        if ektot_match:
            ektot_values.append(float(ektot_match.group(1)))
    
    # Ignore the first and last two values
    nstep_values = nstep_values[:-3]
    etot_values = etot_values[:-2]
    temp_values = temp_values[:-3]
    ektot_values = ektot_values[:-3]
    
    return nstep_values, etot_values, ektot_values, temp_values

def plot_results(nstep_values, etot_values, ektot_values, temp_values):
    plt.figure(figsize=(12, 6))

    # Plot Etot vs NSTEP
    plt.subplot(1, 3, 1)
    plt.plot(nstep_values, etot_values, marker='o', linestyle='-', color='b')
    #plt.ylim(-65000,-45000)
    plt.xlabel('NSTEP')
    plt.ylabel('Etot')
    plt.title('Etot vs NSTEP')
    
    # Plot Etot vs NSTEP
    plt.subplot(1, 3, 2)
    plt.plot(nstep_values, ektot_values, marker='o', linestyle='-', color='g')
    #plt.ylim(-65000,-45000)
    plt.xlabel('NSTEP')
    plt.ylabel('EKtot')
    plt.title('EKtot vs NSTEP')
    
    # Plot TEMP(K) vs NSTEP
    plt.subplot(1, 3, 3)
    plt.plot(nstep_values, temp_values, marker='o', linestyle='-', color='r')
    #plt.ylim(100,450)
    plt.xlabel('NSTEP')
    plt.ylabel('TEMP(K)')
    plt.title('TEMP(K) vs NSTEP')

    plt.tight_layout()
    plt.show()


nstep_values, etot_values, ektot_values, temp_values = read_equil_out('equil_QM.out')
plot_results(nstep_values, etot_values, ektot_values, temp_values)

print("NSTEP values:", nstep_values)
print("Etot values:", etot_values)
print("EKtot values:", ektot_values)
print("TEMP(K) values:", temp_values)


