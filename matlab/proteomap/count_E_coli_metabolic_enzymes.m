% Counting metabolic enzymes in E coli

resource_dir = '/home/wolfram/projekte/proteomaps/online_paver/online_paver_2.0/';
organism_mapping_file = [resource_dir '/organism_mapping/eco_mapping.csv'];

dum = load_any_table(organism_mapping_file);
mapping.genes         = dum(:,1);
mapping.protein_short = dum(:,2);
mapping.ko_number     = dum(:,3);
mapping.protein_long  = dum(:,2);

hierarchy_file      = [resource_dir 'KO_gene_hierarchy_2014.tms'];
ko_tree = load_file_as_strings(hierarchy_file);
ko_tree = ko_tree_shift_one_level_up(ko_tree);
[kko_tree,ko_list] = ko_tree_select_subtree(ko_tree,'Metabolism')
length(find(label_names(unique(ko_tree_extract_ko_list(kko_tree)),mapping.ko_number)))
