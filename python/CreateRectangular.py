# ----------------------------------------------------------------
# Call matlab program to create rectangular treemaps
# ----------------------------------------------------------------

import sys
import os
import subprocess
import argparse
import re
import csv
from proteomaps_PATHNAMES import proteomaps_PATHNAMES

# ----------------------------------------------------------------
# Command line arguments

parser = argparse.ArgumentParser(description='Make rectangle proteomaps')
parser.add_argument('data_dir', help='directory name (full path) for data set bundle')
parser.add_argument('hierarchy_version', help='subdirectory containing the hierarchy data to be used')
args = parser.parse_args()

a = proteomaps_PATHNAMES(args.hierarchy_version)
MATLAB_PATH   = a.MATLAB_PATH

# ----------------------------------------------------------------
# Call matlab program to create rectangular treemaps

p = subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-nodisplay', '-r "addpath(genpath(\'' + MATLAB_PATH + '\')); BASE_DIR = \'' + a.BASE_DIR + '\'; TMP_DIR = \'' + a.TMP_DIR + '\'; RESOURCE_DIR = \'' + a.PROTEIN_HIERARCHY_DIR + '\'; data_directory = \'' + args.data_dir + '\'; proteomaps_path_names; proteomap_treemap; quit;"'])
p.wait()
