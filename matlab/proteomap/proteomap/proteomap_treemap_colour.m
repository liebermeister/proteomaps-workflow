function proteomap_treemap_colour(data_file,organism,options)

% proteomap_treemap_colour(data_file,organism,options)

% this is supposed to work with input files like those in online paver 2.0

if 0,
  data_file = '~/projekte/proteomaps/online_paver/example_data_sets_for_online_paver/sce_Nagaraj_cost.csv';
  proteomap_treemap_colour(data_file,'sce');
end

eval(default('options','struct'));

resource_dir = '/home/wolfram/projekte/proteomaps/online_paver/online_paver_2.0/';

switch organism,
  case 'sce',
    options_def.organism_mapping_file = [resource_dir '/organism_mapping/sce_mapping.csv'];
  otherwise 
    error('unknown organism');
end

options_def.hierarchy_file      = [resource_dir 'KO_gene_hierarchy_2014.tms'];

% ------------------------------------------------
% Options

options_def.color_scale         = 'log';
options_def.fontcolor           = [1 1 1];
options_def.size_by_values      = 0;
options_def.colormap            = flipud(copper(100));
options_def.show_level          = 3; % level of category labels to be shown:  2=lv2; 3=lv3; 4=genes; 5=no labels
options_def.strong_lines        = 1; % emphasize 3rd level categories by stronger lines
options_def.rect                = [0 1 0 1]; % total rectangle: left right bottom top
options_def.capitalize          = 1; % write all protein names with capital first letter?
options_def.protein_minimal_size_for_label = 0.001;

options = join_struct(options_def, options);

% -----------------------------------------------
% prepare data

if isstr(data_file),
  dum = load_any_table(data_file);
  data.genes   = dum(:,1);
  data.numbers = cell_string2num(dum(:,2));
else 
  data = data_file;
end

ind = find(isfinite(data.numbers));
data.genes   = data.genes(ind);
data.numbers = data.numbers(ind);

dum = load_any_table(options.organism_mapping_file);
mapping.genes         = dum(:,1);
mapping.protein_short = dum(:,2);
mapping.ko_number     = dum(:,3);
mapping.protein_long  = dum(:,2);

ll             = label_names(data.genes,mapping.genes);
data.genes     = data.genes(find(ll));
data.numbers   = data.numbers(find(ll));
data.ko_number = mapping.ko_number(ll(find(ll)));

ko_tree = load_file_as_strings(options.hierarchy_file);
ko_tree = ko_tree_shift_one_level_up(ko_tree); % remove the top-level node and shift all nodes one level up
ko_list = ko_tree_extract_ko_list(ko_tree);

% prepare vectors of relevant KO ids and data values (summed over proteins belonging to each KO id)
numbers = zeros(size(ko_list));
for it = 1:length(ko_list),
  ll = find(strcmp(ko_list{it}, data.ko_number));
  numbers(it) = sum(data.numbers(ll));
end
my_ko_list = ko_list(find(numbers));
my_numbers = numbers(find(numbers));

if options.size_by_values, 
  summed_sizes = protein_abundance_branch_ratios_cumulative(ko_tree,my_ko_list,my_numbers);
else
  summed_sizes = protein_abundance_branch_ratios_cumulative(ko_tree,my_ko_list,ones(size(my_numbers)));
end

names        = strrep(ko_tree,sprintf('\t'),'');
levels       = cellfun('length',strfind(ko_tree,sprintf('\t'))) +1;

% -----------------------------------------------
% arrangement

fixed_arrangement  = 0;          % use the same arrangement for all frames (not recommended here)
split_direction    = 'flexible'; % overridden by 'fixed arrangement'
if fixed_arrangement, split_direction = 'horizontal'; end

% -----------------------------------------------
% color scale

switch options.color_scale, 
  case 'linear'
    my_numbers_normalised = my_numbers / max(my_numbers);
  case 'log',
    my_numbers_normalised = [log(my_numbers) - min(log(my_numbers))] / [max(log(my_numbers)) - min(log(my_numbers))];
  end

colortable.names  = my_ko_list;
colortable.colors = options.colormap(1+floor([size(options.colormap,1)-1]*my_numbers_normalised),:);

% -----------------------------------------------
% compute treemap 

show_names = names;

[names_c,summed_sizes_c,colors_c,levels_c, show_names_c] = treemap_prepare_data(names,levels,summed_sizes,colortable,show_names);

rects = treemap_hierarchical(options.rect,names_c,summed_sizes_c,colors_c,levels_c,split_direction,fixed_arrangement);

% -----------------------------------------------
% graphics 

figure(1); set(gcf,'Position',[120,20,1000,1000]); clf;

treemap_plot(levels_c,names_c,rects,colors_c,show_names_c,...
	     struct('shift_text',0,'fontsize',10,'show_level',options.show_level,...
		    'strong_lines',options.strong_lines,'sample_label',organism,...
		    'protein_minimal_size_for_label',options.protein_minimal_size_for_label,...
		    'fontcolor',options.fontcolor));  
