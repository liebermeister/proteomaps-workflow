function proteomap_colormap(data_directory, pathnames, show_graphics)

% proteomap_colormap(data_directory, pathnames, show_graphics)
%
% generate proteomap colormap (wrapper function around 'make_protein_colormap')
  
eval(default('pathnames','[]','show_graphics','1'));

if isempty(pathnames),
  pathnames = proteomaps_path_names(data_directory);
end

display(['Using data sets from directory ' data_directory]);

infile    = [ data_directory '/hierarchy/KO_hierarchy_standardised.tms'];
outfile   = [ data_directory '/hierarchy/KO_color_table.csv'];
colorfile = [ pathnames.PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv'];

make_protein_colormap(infile,outfile,colorfile, show_graphics);
