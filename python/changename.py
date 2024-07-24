#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:11:41 2024

@author: enp
"""

import os

# List of file names
file_names = [
    "HO5'_0.01eV_14.15Aps.rst", "HO5'_0.14eV_52.12Aps.rst", "HO5'_0.27eV_72.27Aps.rst", "HO5'_0.40eV_87.90Aps.rst",
    "HO5'_0.02eV_19.89Aps.rst", "HO5'_0.15eV_53.94Aps.rst", "HO5'_0.28eV_73.59Aps.rst", "HO5'_0.41eV_88.99Aps.rst",
    "HO5'_0.03eV_24.29Aps.rst", "HO5'_0.16eV_55.70Aps.rst", "HO5'_0.29eV_74.89Aps.rst", "HO5'_0.42eV_90.06Aps.rst",
    "HO5'_0.04eV_28.00Aps.rst", "HO5'_0.17eV_57.41Aps.rst", "HO5'_0.30eV_76.16Aps.rst", "HO5'_0.43eV_91.13Aps.rst",
    "HO5'_0.05eV_31.27Aps.rst", "HO5'_0.18eV_59.06Aps.rst", "HO5'_0.31eV_77.42Aps.rst", "HO5'_0.44eV_92.18Aps.rst",
    "HO5'_0.06eV_34.23Aps.rst", "HO5'_0.19eV_60.67Aps.rst", "HO5'_0.32eV_78.65Aps.rst", "HO5'_0.45eV_93.21Aps.rst",
    "HO5'_0.07eV_36.94Aps.rst", "HO5'_0.20eV_62.24Aps.rst", "HO5'_0.33eV_79.87Aps.rst", "HO5'_0.46eV_94.24Aps.rst",
    "HO5'_0.08eV_39.47Aps.rst", "HO5'_0.21eV_63.77Aps.rst", "HO5'_0.34eV_81.06Aps.rst", "HO5'_0.47eV_95.26Aps.rst",
    "HO5'_0.09eV_41.85Aps.rst", "HO5'_0.22eV_65.27Aps.rst", "HO5'_0.35eV_82.24Aps.rst", "HO5'_0.48eV_96.26Aps.rst",
    "HO5'_0.10eV_44.10Aps.rst", "HO5'_0.23eV_66.73Aps.rst", "HO5'_0.36eV_83.40Aps.rst", "HO5'_0.49eV_97.26Aps.rst",
    "HO5'_0.11eV_46.24Aps.rst", "HO5'_0.24eV_68.15Aps.rst", "HO5'_0.37eV_84.55Aps.rst", "HO5'_0.50eV_98.24Aps.rst",
    "HO5'_0.12eV_48.28Aps.rst", "HO5'_0.25eV_69.55Aps.rst", "HO5'_0.38eV_85.68Aps.rst",
    "HO5'_0.13eV_50.24Aps.rst", "HO5'_0.26eV_70.93Aps.rst", "HO5'_0.39eV_86.80Aps.rst"
]

# Directory containing the files
directory = "modified_restart_files"

# Rename the files
for old_name in file_names:
    new_name = old_name.replace("'", "")
    os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
    print(f'Renamed: {old_name} to {new_name}')
