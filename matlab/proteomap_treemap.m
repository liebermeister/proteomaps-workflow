% ----------------------------------------------
%% IN DER FUNKTION TREE_SIZES IST VERMUTLICH NOCH IRGENDEIN FEHLER
%% .. DAHER LIEBER cumulative_values VERWENDEN
%%sizes        = nan*zeros(size(names)); sizes(levels==4) = X(:,ind_data_set);
%%summed_sizes = tree_sizes(levels,sizes);

if 0,  
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_khan_human_chimp'; proteomap_treemap

  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_krizhanovsky'; proteomap_treemap

  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_paper'; proteomap_treemap
  
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_other'; proteomap_treemap
end

% load preprocessed data (see protein_abundance_read_data)
% variables: cumulative_value; ko_tree protein_data.data_sets_short

nnn       = findstr('/', data_directory);
data_sets = data_directory(nnn(end)+1:end);
infile    = [ data_sets '_read_data_protein_lengths' ]; load(infile);
                                                                   
options.fixed_arrangement = 1;
options.split_direction   = 'flexible'; % overridden by fixed arrangement
options.color_file        = [data_directory '/hierarchy/KO_color_table.csv'];
options.output_directory  =  '~/projekte/protein_abundance/ps-files/rectangular_proteomaps';
options.show_level        = 3;

proteomap_draw_treemap(ko_tree, cumulative_value, protein_data.data_sets_short, options);
