proteomaps_path_names;

if 0,
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_khan_human_chimp';  show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_paper';  show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_others'; show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_geiger_mouse'; show_protein_colormap;
end

display(['Using data sets from directory  ' data_directory]);

infile    = [ data_directory '/hierarchy/KO_hierarchy_standardised.tms'];
outfile   = [ data_directory '/hierarchy/KO_color_table.csv'];
colorfile = [ PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv'];

make_protein_colormap(infile,outfile,colorfile);
