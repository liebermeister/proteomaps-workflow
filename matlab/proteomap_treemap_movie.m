% ----------------------------------------------
% Proteomaps movie
%
% Eventuelle verbesserung .. am anfang auf jeder kategorieebene die gene der "groesse" nach anordnen (mittelwert ueber die zeitreihe)???

addpath(genpath('/home/wolfram/Proteomaps/matlab/'))

% data_directory    = '/home/wolfram/Proteomaps/data_sets/protein_abundances_valgepea_ecoli/';
% data_set_short    = 'eco_Valgepea';
% data_sets         = 'protein_abundances_valgepea_ecoli';
% show_data_sets    = {'eco Valgepea 2013 11','eco Valgepea 2013 21','eco Valgepea 2013 31','eco Valgepea 2013 40','eco Valgepea 2013 48'}; % see table(protein_data.data_sets_short)

data_set_short    = 'mpn_Lluch';
data_directory    = '/home/wolfram/projekte/protein_abundance/Proteomaps_DEVELOPMENT_VERSION/data_sets/protein_abundances_mycoplasma_pneumoniae_lluch/';
data_sets         = 'protein_abundances_mycoplasma_pneumoniae_lluch';
show_data_sets    = {'mpn Lluch 1 0 25h', 'mpn Lluch 2 0 5h', 'mpn Lluch 3 1h', 'mpn Lluch 4 2h', 'mpn Lluch 5 6h', 'mpn Lluch 6 8h','mpn Lluch 7 10h', 'mpn Lluch 8 12h', 'mpn Lluch 9 24h', 'mpn Lluch 10 36h', 'mpn Lluch 11 48h', 'mpn Lluch 12 72h', 'mpn Lluch 13 96h'}; % see table(protein_data.data_sets_short)

%proteomaps_path_names
PROTEOMAPS_MATLAB_DATA_DIR = [data_directory '/tables/'];

show_black_frames  = 5; % number of black frames at the end of the movie (for loops)
show_sample_labels = 1;
rect               = [0 1 0 1]; % left right bottom top
fixed_arrangement  = 1;
split_direction    = 'flexible'; % overridden by fixed arrangement
output_directory   = '~/projekte/protein_abundance/ps-files/rectangular_proteomaps/movies';
color_file         = ['~/projekte/protein_abundance/Proteomaps_DEVELOPMENT_VERSION/data_sets/'  data_sets '/hierarchy/KO_color_table.csv'];
%color_file        = ['~/projekte/protein_abundance/proteomaps_data_sets/' data_sets '/hierarchy/KO_color_table.csv'];

% -----------------------------------------------
% load preprocessed data (see protein_abundance_read_data)
% variables cumulative_value; ko_tree

infile  = [PROTEOMAPS_MATLAB_DATA_DIR '/' data_sets '_read_data_protein_lengths'];
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
t_interpolated = [0:0.01:1];
D              = interp1([0:1/(n_data_sets-1):1],Summed_sizes',t_interpolated)';

% labels for interpolated values:
frame_sample_names = show_data_sets(1 + ceil(t_interpolated * (n_data_sets-1)));

clear M;

for itt = 1:size(D,2)

  summed_sizes = D(:,itt);
  %% compute treemap 
  [names_c,summed_sizes_c,colors_c,levels_c] = treemap_prepare_data(names,levels,summed_sizes,colortable);
  rects = treemap_hierarchical(rect,names_c,summed_sizes_c,colors_c,levels_c,split_direction,fixed_arrangement);
  
  %% graphics 
  figure(1); set(gcf,'Position',[120,20,1000,1000]); clf;
  treemap_plot(levels_c,names_c,rects,colors_c,struct('shift_text',0,'fontsize',6,'show_level',3));  
  if show_sample_labels,
    text(0.01,0.01,frame_sample_names{itt},'FontSize',16);
  end

  M(itt) = getframe;
  
end

for itb = 1:show_black_frames,
  figure(1); set(gcf,'Position',[120,20,1000,1000]); clf; noticks
  set(gca,'Color',[.2, .2, .2]);
  M(itt+itb) = getframe;
end

cd(output_directory);

movie_save(['proteomap_movie_' strrep(data_set_short,' ','_')],M);
display(sprintf('in directory %s',output_directory));