function protein_abundance(data_directory, n_randomised_trees, pathnames, show_graphics)

eval(default('pathnames','[]','show_graphics','1'))

if isempty(pathnames),
  pathnames = proteomaps_path_names(data_directory);
end
  
% ----------------------------------------------------------------------
% read protein data and save them in .mat file (called by protein_abundance.m)
% make sure that everything is up to date (script README in data directory has been run)
% ----------------------------------------------------------------------

% This script is called from the commandline; 
% so the variable 'data_directory' MUST BE SET, for instance:  
% data_directory = '/home/wolfram/projekte/proteomaps/data/protein_abundances_paper';

if ~exist('verbose','var'),
  verbose = 0;
end

%n_randomised_trees = 1000;
%n_randomised_trees = 10;

protein_lengths = 0;
[data_sets] = protein_abundance_read_data(data_directory,protein_lengths,n_randomised_trees,pathnames);

protein_lengths = 1;
[data_sets] = protein_abundance_read_data(data_directory,protein_lengths,n_randomised_trees,pathnames);

% -------------------------------------------------------------------
% make pictures and tables
% display('Make sure that "protein_abundance_read_data" has been run on the data');

protein_lengths = 0;
protein_abundance_branch_ratios(data_directory,data_sets,protein_lengths,pathnames, show_graphics);

protein_lengths = 1;
protein_abundance_branch_ratios(data_directory,data_sets,protein_lengths,pathnames, show_graphics);

% ---------------------------------------------------------

% protein_abundance_not_mapped;
