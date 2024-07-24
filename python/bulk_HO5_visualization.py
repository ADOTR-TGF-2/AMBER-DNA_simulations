from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
from ovito.pipeline import *
from ovito.vis import *
from ovito.qt_compat import QtCore
import glob

# List of PDB files
pdb_files = glob.glob('/home/enp/amber/amber22/DNA_simulations/Shepard_et_al/*.pdb')
# Sort files lexicographically
pdb_files = sorted(pdb_files)

def process_pdb_file(pdb_file):
    # Data import:
    pipeline = import_file(pdb_file, multiple_frames = True)

    # Visual element initialization:
    data = pipeline.compute() # Evaluate new pipeline to gain access to visual elements associated with the imported data objects.
    data.particles.bonds.vis.enabled = False
    data.cell.vis.enabled = False
    del data # Done accessing input DataCollection of pipeline.
    pipeline.add_to_scene()


    # Modifier group - Select type:
    pipeline.modifiers.append(SelectTypeModifier(
        property = 'Residue Type', 
        types = {8}))

    # Modifier group - Compute property:
    pipeline.modifiers.append(ComputePropertyModifier(
        expressions = ('0.9',), 
        output_property = 'Transparency', 
        only_selected = True))

    # Modifier group - Assign color:
    pipeline.modifiers.append(AssignColorModifier(color = [0.3333333432674408, 0.6666666865348816, 1.0]))


    # Modifier group - Select type:
    pipeline.modifiers.append(SelectTypeModifier(
        property = 'Atom Name', 
        types = {1}))


    # Modifier group - Assign color:
    pipeline.modifiers.append(AssignColorModifier(color = [0.0, 0.0, 0.0]))

    # Viewport setup:
    vp = Viewport(
        type = Viewport.Type.Ortho, 
        fov = 34.7195618176, 
        camera_dir = [0.9068678995737008, -0.20103517389784392, 0.37037207181245146], 
        camera_pos = [29.976, 33.176500000000004, 33.266000000000005])

for pdb_file in pdb_files:
    process_pdb_file(pdb_file)