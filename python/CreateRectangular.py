import sys
import os
import subprocess
import argparse
import re
import csv

# ----------------------------------------------------------------
# Command line arguments

parser = argparse.ArgumentParser(description='Make rectangle proteomaps')
parser.add_argument('data_dir', help='directory name (full path) for data set bundle')
args = parser.parse_args()

# ----------------------------------------------------------------
# Call matlab program to create rectangular treemaps

p = subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-nodisplay', '-r "data_directory = \'' + args.data_dir + '\'; proteomap_treemap; quit;"'])
p.wait()
