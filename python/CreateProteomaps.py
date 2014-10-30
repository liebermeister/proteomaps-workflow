import sys
import os
import subprocess
import argparse
import re
import csv
import pymatlab

from proteomaps_PATHNAMES import proteomaps_PATHNAMES
from map_protein_data import map_protein_data
from filter_ko_hierarchy import filter_ko_hierarchy
from filter_ko_hierarchy_mult import filter_ko_hierarchy_mult
from organism_standardise_mappings import organism_standardise_mappings
from organism_standardised_hierarchy import organism_standardised_hierarchy
from prune_nonmapped_proteins import prune_nonmapped_proteins
from make_csv_tables import make_csv_tables

# ----------------------------------------------------------------
# Command line arguments

parser = argparse.ArgumentParser(description='Data processing workflow for proteomaps')
parser.add_argument('data_dir',   help='directory name (full path) for data set bundle')
parser.add_argument('paver_files_directory', help='directory name (full path) for proteomaps output files')
parser.add_argument('n_annotation_subsampling', help='number of subsampled hierarchy trees')

args = parser.parse_args()

data_dir                 = args.data_dir 
n_annotation_subsampling = int(args.n_annotation_subsampling)
paver_files_directory    = args.paver_files_directory

# ----------------------------------------------------------------
# Path names

a             = proteomaps_PATHNAMES()
WORKFLOW_PATH = a.WORKFLOW_PATH
MATLAB_PATH   = a.MATLAB_PATH

# ----------------------------------------------------------------
# Run workflow (python functions)

map_protein_data(data_dir)

filter_ko_hierarchy(data_dir)

filter_ko_hierarchy_mult(data_dir, n_annotation_subsampling)

organism_standardise_mappings(data_dir)

organism_standardised_hierarchy(data_dir)

prune_nonmapped_proteins(data_dir)

make_csv_tables(data_dir)

# ---------------------------------------------------------------
# Run MATLAB scripts

matlab_session = pymatlab.session_factory("-nojvm -nodisplay")

# Make colormap with matlab

print('Preparing color map');

matlab_session.run( "addpath(genpath('" + MATLAB_PATH + "'))" )
matlab_session.run( "data_directory = '" + data_dir + "'" )
matlab_session.run( "show_protein_colormap"  )

# Create result tables with matlab

print('Preparing result table');

matlab_session.run( "n_randomised_trees = " + str(n_annotation_subsampling) )
matlab_session.run( "protein_abundance" )

del matlab_session

# ---------------------------------------------------------------
# Data for Paver

p = subprocess.Popen(['python', WORKFLOW_PATH + '/prepare_files_for_paver.py', data_dir, paver_files_directory])
p.wait()
