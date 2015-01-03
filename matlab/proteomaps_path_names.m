% previously defined: 
% BASE_DIR     e.g. /home/wolfram/Proteomaps/
% TMP_DIR      e.g. /home/wolfram/tmp/matlab_protein_abundance/
% RESOURCE_DIR e.g. /home/wolfram/Proteomaps/genomic_data/KO_gene_hierarchy_2014-08-01/

PROTEOMAPS_MATLAB_DIR      = [BASE_DIR '/matlab'];
PROTEOMAPS_MATLAB_DATA_DIR = [BASE_DIR '/matlab/data/'];
PROTEOMAPS_RESOURCE_DIR    = RESOURCE_DIR;
PROTEIN_LENGTH_DIR         = [BASE_DIR '/genomic_data/protein_length_data/'];
SUBSAMPLED_TREE_DIR        = TMP_DIR;

addpath(genpath(PROTEOMAPS_MATLAB_DIR));
