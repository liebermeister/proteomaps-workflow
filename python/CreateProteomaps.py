import sys
import os
import subprocess
import argparse
import re
import csv
from proteomaps_PATHNAMES import proteomaps_PATHNAMES

# ----------------------------------------------------------------
# Command line arguments

parser = argparse.ArgumentParser(description='Data processing workflow for proteomaps')
parser.add_argument('data_dir',   help='directory name (full path) for data set bundle')
parser.add_argument('paver_files_directory', help='directory name (full path) for proteomaps output files')
parser.add_argument('n_annotation_subsampling', help='number of subsampled hierarchy trees')
args = parser.parse_args()

# ----------------------------------------------------------------
# Path names

a = proteomaps_PATHNAMES()
WORKFLOW_PATH = a.WORKFLOW_PATH
MATLAB_PATH   = a.MATLAB_PATH

# ----------------------------------------------------------------
# Run python scripts

p = subprocess.Popen(['python', WORKFLOW_PATH + 'map_protein_data.py', args.data_dir])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'filter_ko_hierarchy.py', args.data_dir])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'filter_ko_hierarchy_mult.py', args.data_dir, args.n_annotation_subsampling])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'organism_standardise_mappings.py', args.data_dir])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'organism_standardised_hierarchy.py', args.data_dir])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'prune_nonmapped_proteins.py', args.data_dir])
p.wait()

p = subprocess.Popen(['python', WORKFLOW_PATH + 'make_tsv_tables.py', args.data_dir])
p.wait()


# ---------------------------------------------------------------
# Run MATLAB scripts

# Make colormap with matlab
# Command: matlab -nodesktop -nosplash -nodisplay -r "data_directory = '<DIR>'; show_protein_colormap; quit;"
p = subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-nodisplay', '-r "addpath(genpath(\'' + MATLAB_PATH + '\')); data_directory = \'' + args.data_dir + '\'; show_protein_colormap; quit;"'])
p.wait()

# Create result tables with matlab
# Command: matlab -nodesktop -nosplash -nodisplay -r "data_directory = '<DIR>'; n_randomised_trees = '<N>'; protein_abundance; quit;"

p = subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-nodisplay', '-r "addpath(genpath(\'' + MATLAB_PATH + '\')); data_directory = \'' + args.data_dir + '\'; n_randomised_trees = ' + args.n_annotation_subsampling + '; protein_abundance; quit;"'])
p.wait()

# ---------------------------------------------------------------
# Data for Paver

p = subprocess.Popen(['python', WORKFLOW_PATH + '/prepare_files_for_paver.py', args.data_dir, args.paver_files_directory])
