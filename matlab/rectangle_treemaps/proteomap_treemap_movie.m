% ----------------------------------------------
% Proteomaps movie
%
% Eventuelle verbesserung .. am anfang auf jeder kategorieebene die gene der "groesse" nach anordnen (mittelwert ueber die zeitreihe)???

data_set_short    = 'eco_Valgepea';
data_sets         = 'protein_abundances_valgepea_ecoli';

show_data_sets    = {'eco Valgepea 2013 11','eco Valgepea 2013 21','eco Valgepea 2013 31','eco Valgepea 2013 40','eco Valgepea 2013 48'}; % see table(protein_data.data_sets_short)

rect              = [0 1 0 1]; % left right bottom top
fixed_arrangement = 1;
split_direction   = 'flexible'; % overridden by fixed arrangement
output_directory  = '~/projekte/protein_abundance/ps-files/rectangular_proteomaps/movies';

color_file        = ['~/projekte/protein_abundance/proteomaps_data_sets/' data_sets '/hierarchy/KO_color_table.csv'];

% -----------------------------------------------
% load preprocessed data (see protein_abundance_read_data)
% variables cumulative_value; ko_tree

infile            = ['/home/wolfram/projekte/protein_abundance/proteomaps_code/matlab/data/' data_sets '_read_data_protein_lengths'];
load(infile);


% -----------------------------------------------
% load color table

CT                = load_any_table(color_file);
colortable.names  = CT(:,1);
colortable.colors = cell_string2num(CT(:,2:4));

if fixed_arrangement,
  split_direction = 'horizontal';
end

ind_data_sets = label_names(show_data_sets,protein_data.data_sets_short);
n_data_sets = length(ind_data_sets);

names          = strrep(ko_tree,sprintf('\t'),'');
levels         = cellfun('length',strfind(ko_tree,sprintf('\t'))) +1;
Summed_sizes   = cumulative_value(:,ind_data_sets);

% interpolated values
D              = interp1([0:1/(n_data_sets-1):1],Summed_sizes',[0:0.02:1])';

clear M;

for itt = 1:size(D,2)

  summed_sizes = D(:,itt);
  %% compute treemap 
  [names_c,summed_sizes_c,colors_c,levels_c] = treemap_prepare_data(names,levels,summed_sizes,colortable);
  rects = treemap_hierarchical(rect,names_c,summed_sizes_c,colors_c,levels_c,split_direction,fixed_arrangement);
  
  %% graphics 
  figure(1); set(gcf,'Position',[120,20,1000,1000]); clf;
  treemap_plot(levels_c,names_c,rects,colors_c,struct('shift_text',0,'fontsize',6,'show_level',3));  
  M(itt) = getframe;
  
end

cd(output_directory);

movie_save(['proteomap_movie_' strrep(data_set_short,' ','_')],M);
