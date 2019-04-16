function pathnames = proteomaps_path_names(data_directory)

pathnames.BASE_DIR              = [fileparts(which(mfilename)) filesep '..' filesep];
pathnames.PROTEIN_LENGTH_DIR    = [pathnames.BASE_DIR '/genomic_data/protein_length_data/'];
pathnames.PROTEOMAPS_MATLAB_DIR = [pathnames.BASE_DIR '/matlab'];

pathnames.TMP_DIR  = [tempdir '/matlab_protein_abundance'];
[~,~] = mkdir(pathnames.TMP_DIR);

if ~exist('hierarchy_version','var'),
  pathnames.hierarchy_version = 'KO_gene_hierarchy_2015-01-01';
end

if ~exist('RESOURCE_DIR','var'),
  pathnames.RESOURCE_DIR       = [pathnames.BASE_DIR 'genomic_data/' pathnames.hierarchy_version '/'];
end

pathnames.PROTEOMAPS_RESOURCE_DIR = pathnames.RESOURCE_DIR;
pathnames.SUBSAMPLED_TREE_DIR     = pathnames.TMP_DIR;

pathnames.PROTEOMAPS_MATLAB_DATA_DIR = [data_directory '/tables/'];
