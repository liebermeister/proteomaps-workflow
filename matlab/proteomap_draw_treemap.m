function proteomap_draw_treemap(ko_tree,cumulative_values,data_sets_short,options)

% ko_tree           list of strings
% cumulative_values matrix of abundance values (rows correspond to ko_tree, columns to data sets)
% data_sets_short   short names of data sets (only used for filenames)
%
% fields of "options"
% options.compute_cumulative = 0 If this flag is set, the input argument cumulative_values
%                                contains leaf-related values (instead of precomputed, 
%                                branch and leaf - related values
% options.leaf_ids           list of leaf ids (mandatory argument if previous flag is set)
%                            the leaf ids must correspond to 4th-level entries in ko_tree
% options.rect               = [0 1 0 1];  initial rectangle: left right bottom top 
% options.fixed_arrangement  = 1;
% options.split_direction    = 'flexible'; % overridden by fixed arrangement
% options.color_file         = [data_directory '/hierarchy/KO_color_table.csv'];
% options.output_directory   = directory for picture files
% options.show_level         = 2; level for category labels

% ------------------------------------------------
% further options

default_options.rect               = [0 1 0 1]; % left right bottom top
default_options.fixed_arrangement  = 1;
default_options.split_direction    = 'flexible'; % overridden by fixed arrangement
default_options.compute_cumulative = 0;
default_options.output_directory   = [];

options = join_struct(default_options, options);

if options.compute_cumulative,
  cumulative_values = protein_abundance_branch_ratios_cumulative(ko_tree,options.leaf_ids,cumulative_values);
end

% -----------------------------------------------
% initialise

names          = strrep(ko_tree,sprintf('\t'),'');
levels         = cellfun('length',strfind(ko_tree,sprintf('\t'))) +1;

if options.fixed_arrangement,
  split_direction = 'horizontal';
end

% load color table

CT                = load_any_table(options.color_file);
colortable.names  = CT(:,1);
colortable.colors = cell_string2num(CT(:,2:4));


% -----------------------------------------------

for itt = 1:length(data_sets_short),
  
  data_set_short = data_sets_short{itt};
  summed_sizes   = cumulative_values(:,itt);

  %% compute treemap 
  [names_c,summed_sizes_c,colors_c,levels_c] = treemap_prepare_data(names,levels,summed_sizes,colortable);
  rects = treemap_hierarchical(options.rect,names_c,summed_sizes_c,colors_c,levels_c,split_direction,options.fixed_arrangement);
  
  %% graphics 
  figure(itt); set(gcf,'Position',[120,20,1000,1000]); clf;
  names_c = strrep(names_c,'_',' ');
  treemap_plot(levels_c,names_c,rects,colors_c,options);  
 
  if length(options.output_directory),
    cd(options.output_directory);
    exportfig(itt,['proteomap_' strrep(data_set_short,' ','_') '_lv' num2str(options.show_level) '.eps'],'Color','rgb')
    display(['Writing graphics to file ', options.output_directory, '/proteomap_' strrep(data_set_short,' ','_') '_lv' num2str(options.show_level) '.eps']);
  end
  
  title(data_set_short)
end
