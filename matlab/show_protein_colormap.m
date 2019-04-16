function show_protein_colormap(data_directory,pathnames)

if 0,
  data_directory = '/home/wolfram/Proteomaps/data_sets/protein_abundances_paper';  show_protein_colormap;
end

display(['Using data sets from directory  ' data_directory]);

infile    = [ data_directory '/hierarchy/KO_hierarchy_standardised.tms'];
outfile   = [ data_directory '/hierarchy/KO_color_table.csv'];
colorfile = [ pathnames.PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv'];

make_protein_colormap(infile,outfile,colorfile);
