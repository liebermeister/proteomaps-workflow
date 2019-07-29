function proteomap_treemap_movie(organism, data_directory, movie_file, options)

% proteomap_treemap_movie(organism, data_directory, movie_file, options)
%
% Rectangle proteomap movie
%
% Default options:
%
% options.show_level          = 3;  % level of category labels to be shown:  2=lv2; 3=lv3; 4=genes; 5=no labels
% options.strong_lines        = 1;  % emphasize 3rd level categories by stronger lines
% options.rect                = [0 1 0 1]; % total rectangle: left right bottom top
% options.color_file          = [ data_directory '/hierarchy/KO_color_table.csv' ];
% options.matlab_data_dir     = [ data_directory '/tables/' ]; % path name for prepared data (.mat files)
% options.mapping_file        = [ data_directory '/hierarchy/' organism '_mapping_final.csv' ];
% options.capitalize          = 1; % write all protein names with capital first letter?
% options_def.output_directory = [];
% options.interpolation_steps = 25; % number of interpolation intervals = number of frames - 1
% options.movie_duration      = 8;  % movie duration in seconds
% options.show_black_frames   = 5;  % number of black frames at the end of the movie (for loops)
% options.omit_not_mapped     = 1;  % flag: omit unmapped genes
% options.omit_human_diseases = 1;  % flag: omit genes in "human disease" category
% options.protein_minimal_size_for_label = 0.001;

% Moegliche Verbesserung .. am Anfang auf jeder Kategorieebene
% die Gene der "Groesse" nach anordnen (Mittelwert ueber die Zeitreihe)?

eval(default('options','struct'));

% ------------------------------------------------
% Options

options_def.show_level          = 3; % level of category labels to be shown:  2=lv2; 3=lv3; 4=genes; 5=no labels
options_def.strong_lines        = 1; % emphasize 3rd level categories by stronger lines
options_def.rect                = [0 1 0 1]; % total rectangle: left right bottom top
options_def.color_file          = [ data_directory '/hierarchy/KO_color_table.csv' ];
options_def.matlab_data_dir     = [ data_directory '/tables/' ]; % path name for prepared data (.mat files)
options_def.mapping_file        = [ data_directory '/hierarchy/' organism '_mapping_final.csv' ];
options_def.capitalize          = 1; % write all protein names with capital first letter?
options_def.output_directory    = [];
options_def.interpolation_steps = 25; % # of interpolation intervals = # of frames - 1
options_def.movie_duration      = 8; % seconds
options_def.show_black_frames   = 5; % number of black frames at the end of the movie (for loops)
options_def.omit_not_mapped     = 1;
options_def.omit_human_diseases = 1;
options_def.protein_minimal_size_for_label = 0.001;

%show_sample_labels  = 1; % flag: show sample names on bottom left

% -----------------------------------------------

A = load_any_table([data_directory, '/filenames.csv']);
options_def.show_data_sets    = strrep(A(:,3),'_', ' ');

if ~strcmp(data_directory(end),'/'), data_directory =[ data_directory '/']; end
dum = findstr('/', data_directory);
data_sets = data_directory(dum(end-1)+1:dum(end)-1);

options = join_struct(options_def, options);

% -----------------------------------------------
% load preprocessed data (see protein_abundance_read_data)
% variables cumulative_value; ko_tree

infile  = [options.matlab_data_dir '/' data_sets '_read_data_protein_lengths'];
load(infile);

% -----------------------------------------------
% omit "Not Mapped" region if desired 

if options.omit_not_mapped,
%  ind_keep = find(strcmp('Not Mapped',ko_tree) + ...
%			 strcmp('	Not Mapped',ko_tree) + ...
%			 strcmp('		Not mapped',ko_tree) + ...
%			 strcmp('			NotMapped',ko_tree)==0);
  [~,ind_keep_lines] = ko_tree_remove_branch(ko_tree,'Not Mapped');
  cumulative_value = cumulative_value(ind_keep_lines,:);
  ko_tree = ko_tree(ind_keep_lines);
end

if options.omit_human_diseases,
  [kko_tree,ind_keep_lines] = ko_tree_remove_branch(ko_tree,'Human Diseases');
  cumulative_value = cumulative_value(ind_keep_lines,:);
  ko_tree = ko_tree(ind_keep_lines);
end

% -----------------------------------------------
% load color table

CT                = load_any_table(options.color_file);
colortable.names  = CT(:,1);
colortable.colors = cell_string2num(CT(:,2:4));

% -----------------------------------------------
% arrangement

fixed_arrangement  = 1; % use the same arrangement for all frames
split_direction    = 'flexible'; % overridden by 'fixed arrangement'

if fixed_arrangement,
  split_direction = 'horizontal';
end

ind_data_sets = label_names(options.show_data_sets,protein_data.data_sets_short);
n_data_sets = length(ind_data_sets);

names          = strrep(ko_tree,sprintf('\t'),'');
levels         = cellfun('length',strfind(ko_tree,sprintf('\t'))) +1;
Summed_sizes   = cumulative_value(:,ind_data_sets);

% -----------------------------------------------
% replace KO numbers by gene names where possible
% THIS INSERTS ONLY ONE GENE NAME PER KO NUMBER (=> possible problem with ribosome subunits)

mapping_table = load_any_table(options.mapping_file);
protein_names = {};
systematic_names = {};
% extract protein names (omit systematic names, after colon)
for it = 1:length(mapping_table),
  dum = strsplit(':', mapping_table{it,2});
  protein_names{it,1} = strrep(dum{1},'_','');
  if options.capitalize, 
    protein_names{it,1}(1) = upper(protein_names{it,1}(1));
  end
  %systematic_names{it,2} = dum{2};
end
ll = label_names(names, mapping_table(:,1));
show_names = names; 
show_names(find(ll)) = protein_names(ll(find(ll)));

% -----------------------------------------------
% interpolation in time

t_interpolated = [0:(1/options.interpolation_steps):1];
D              = interp1([0:1/(n_data_sets-1):1],Summed_sizes',t_interpolated,'spline')';

% labels for interpolated values:
frame_sample_names = options.show_data_sets(1 + ceil(t_interpolated * (n_data_sets-1)));

% -----------------------------------------------
% make movie

clear M;

for itt = 1:size(D,2)
  summed_sizes = D(:,itt);

  %% compute treemap 
  [names_c,summed_sizes_c,colors_c,levels_c, show_names_c] = treemap_prepare_data(names,levels,summed_sizes,colortable,show_names);
  rects = treemap_hierarchical(options.rect,names_c,summed_sizes_c,colors_c,levels_c,split_direction,fixed_arrangement);
  
  %% graphics 
  figure(1); set(gcf,'Position',[120,20,1000,1000]); clf;
  treemap_plot(levels_c,names_c,rects,colors_c,show_names_c,struct('shift_text',0,'fontsize',10,'show_level',options.show_level,'strong_lines',options.strong_lines,'sample_label',frame_sample_names{itt},'protein_minimal_size_for_label',options.protein_minimal_size_for_label));  
  M(itt) = getframe;
end

% black frames at the end
for itb = 1:options.show_black_frames,
  figure(1); set(gcf,'Position',[120,20,1000,1000]); clf; noticks
  set(gca,'Color',[.2, .2, .2]);
  M(itt+itb) = getframe;
end

% -----------------------------------------------
% save movie

my_delay = 100*options.movie_duration/options.interpolation_steps; % in 1/100 seconds

[fpath,fname,fext] = fileparts(movie_file);

if length(fpath)==0,
  fpath = options.output_directory;
end

movie_save(sprintf('%s/%s_lv%d%s', fpath,   strrep(fname,' ','_'), options.show_level,fext), M,my_delay);
