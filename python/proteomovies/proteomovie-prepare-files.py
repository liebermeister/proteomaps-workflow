# ----------------------
# Rectangle proteomovies
# ----------------------
#
# python3 proteomovie-prepare-files.py [INPUT FILE] [OUTPUT_FILE] [ORGANIM] [DATA_SET_NAME] [PROTEOMAPS_DIRECTORY]

import tempfile
import os
import argparse
import shutil
from shutil import copyfile
from split_data_file import split_data_file
from CreateProteomaps import CreateProteomaps
from CreateProteomaps_no_matlab import CreateProteomaps_no_matlab

# -----------------------------------------
# make tmp_dir

tmp_dir = tempfile.mkdtemp()

# -----------------------------------------
# read commandline arguments

parser = argparse.ArgumentParser(description='Generate rectangle proteomovie')

parser.add_argument('infile',   help='data file')
parser.add_argument('outfile',  help='proteomovie file')
parser.add_argument('organism', help='KEGG short name of organism (e.g. "eco" for E. coli; see proteomaps documentation)')
parser.add_argument('data_set', help='Name of data set (to be shown in movie; optional)')
parser.add_argument('proteomaps_dir', help='Directory name for proteomaps files created during the process; optional)')

args = parser.parse_args()

infile   = args.infile  
outfile  = args.outfile 
organism = args.organism
data_set = args.data_set

n_annotation_subsampling = 10

# -----------------------------------------
# make filenames

infile_dir, infile_file   = os.path.split(infile)
outfile_dir, outfile_file = os.path.split(outfile)


proteomaps_dir = args.proteomaps_dir
data_dir       = proteomaps_dir + "/csv"       # (for input proteomics data (single csv files))
movie_file     = outfile       # (for input proteomics data)
organism_long  = organism      # (for your convenience)
data_set_long  = data_set      # (for your convenience)

outfile_tmp  = data_dir + "/" + outfile_file

# -----------------------------------------
# make proteomaps data dir if necessary

#if args.proteomaps_dir is not None:
#    proteomaps_dir = args.proteomaps_dir
#else:
#    proteomaps_dir = tmp_dir

if not os.path.exists(proteomaps_dir):
    os.mkdir(proteomaps_dir)

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# -----------------------------------------
# Split table into single data files, with extra information, by using the script split_data_table.py

split_data_file(data_set, infile, outfile_tmp , organism, organism_long, data_set_long)

copyfile(outfile_tmp + '_LOG.csv', proteomaps_dir + '/filenames.csv')

# -----------------------------------------
# Run the proteomaps workflow to generate the .mat files

print("- Generating proteomaps data files - please be patient, this may take a few minutes.")

CreateProteomaps_no_matlab(proteomaps_dir, tmp_dir, n_annotation_subsampling , 'KO_gene_hierarchy_2015-01-01', verbose=0)

print("- Proteomaps data files written to " + proteomaps_dir);
        
print( "- Please start matlab and run the command:\n  proteomovie('" + proteomaps_dir + "','" + movie_file + "'," + str(n_annotation_subsampling) + ");")

#shutil.rmtree(tmp_dir)
