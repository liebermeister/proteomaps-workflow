% --------------------------------------
% read KO tree in KO_hierarchy.csv
% and make versions with lower levels omitted
% --------------------------------------

proteomaps_path_names

KO_tree = load_file_as_strings([ PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy.tms']);

[ko_tree_1, ko_tree_2, ko_tree_3] = ko_tree_remove_leafs(KO_tree);

cd(PROTEOMAPS_RESOURCE_DIR);
table(ko_tree_1,0,'KO_gene_hierarchy_level_1.tms')
table(ko_tree_2,0,'KO_gene_hierarchy_level_2.tms')
table(ko_tree_3,0,'KO_gene_hierarchy_level_3.tms')
