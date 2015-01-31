% ----------------------------------------------------------------------
% read protein data and save them in .mat file (called by protein_abundance.m)
% make sure that everything is up to date (script README in data directory has been run)

% This script is called from the commandline; 
% so the variable 'data_directory' MUST BE SET, for instance:  
% data_directory = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_paper';

proteomaps_path_names;

%n_randomised_trees = 1000;
%n_randomised_trees = 10;

cd(PROTEOMAPS_MATLAB_DIR);
protein_lengths = 0;
protein_abundance_read_data;

cd(PROTEOMAPS_MATLAB_DIR);
protein_lengths = 1;
protein_abundance_read_data;


% -------------------------------------------------------------------
% make pictures and tables
% display('Make sure that "protein_abundance_read_data" has been run on the data');

cd(PROTEOMAPS_MATLAB_DIR);
protein_lengths = 0;
protein_abundance_branch_ratios;

cd(PROTEOMAPS_MATLAB_DIR);
protein_lengths = 1;
protein_abundance_branch_ratios;

% ---------------------------------------------------------

% protein_abundance_not_mapped;
