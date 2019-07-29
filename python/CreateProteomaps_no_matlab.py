import sys
import os
import subprocess
import argparse
import re
import csv
import pymatlab

from proteomaps_PATHNAMES import proteomaps_PATHNAMES
from proteomaps_path_names import proteomaps_path_names
from map_protein_data import map_protein_data
from filter_ko_hierarchy import filter_ko_hierarchy
from filter_ko_hierarchy_mult import filter_ko_hierarchy_mult
from organism_standardise_mappings import organism_standardise_mappings
from organism_standardised_hierarchy import organism_standardised_hierarchy
from prune_nonmapped_proteins import prune_nonmapped_proteins
from make_csv_tables import make_csv_tables

# ----------------------------------------------------------------
# Function CreateProteomaps
# ----------------------------------------------------------------

def CreateProteomaps_no_matlab(data_dir, paver_files_directory, n_annotation_subsampling, hierarchy_version, verbose):

    # ----------------------------------------------------------------
    # Path names
    
    pn            = proteomaps_PATHNAMES(hierarchy_version)
    WORKFLOW_PATH = pn.WORKFLOW_PATH
    MATLAB_PATH   = pn.MATLAB_PATH
    
    # ----------------------------------------------------------------
    # Run workflow (python functions)
    
    pp = proteomaps_path_names(data_dir,hierarchy_version,verbose)
    
    map_protein_data(data_dir,pp)
    
    filter_ko_hierarchy(data_dir,pp)
    
    filter_ko_hierarchy_mult(data_dir, n_annotation_subsampling,pp)
    
    organism_standardise_mappings(data_dir,pp)
    
    organism_standardised_hierarchy(data_dir,pp)
    
    prune_nonmapped_proteins(data_dir,pp)
    
    make_csv_tables(data_dir,pp,pn)


# ---------------------------------------------------------------
# Main routine
# ---------------------------------------------------------------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Data processing workflow for proteomaps')
    parser.add_argument('data_dir',   help='directory name (full path) for data set bundle')
    parser.add_argument('paver_files_directory', help='directory name (full path) for proteomaps output files')
    parser.add_argument('n_annotation_subsampling', help='number of subsampled hierarchy trees')
    parser.add_argument('hierarchy_version', help='subdirectory containing the hierarchy data to be used')
    
    args = parser.parse_args()
    
    data_dir                 = args.data_dir 
    paver_files_directory    = args.paver_files_directory
    n_annotation_subsampling = int(args.n_annotation_subsampling)
    hierarchy_version        = args.hierarchy_version

    verbose = 1
    CreateProteomaps_no_matlab(data_dir, paver_files_directory, n_annotation_subsampling, hierarchy_version, verbose)
