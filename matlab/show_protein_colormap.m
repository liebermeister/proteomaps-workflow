proteomaps_path_names;

if 0,
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_khan_human_chimp';  show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_paper';  show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_others'; show_protein_colormap;
  data_directory = '/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/protein_abundances_geiger_mouse'; show_protein_colormap;
end


% -----------------------------------------------------
% Load and show 2nd-level category colours

%A = load_any_table('/home/wolfram/projekte/protein_abundance/gene_hierarchy/Protein_category_colours_Perfect.csv');

A = load_any_table([ PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv']);

names = A(:,1);
col   = cell_string2num(A(:,2:4));

%col(:,2) = 0.7 * col(:,2) + 0.3 * col(:,2).^2; % change green channel

figure(1); 
im([1:size(col,1)]',[1,size(col,1)],names); colormap(col);


% -----------------------------------------------------

display(['Using data sets from directory  ' data_directory]);

ko_tree = load_file_as_strings([ data_directory '/hierarchy/KO_hierarchy_standardised.tms']);
ko_list = ko_tree_extract_ko_list(ko_tree);

if length(ko_list)-length(unique(ko_list)),
  error('KO ids appear multiple times');
end

[ko_tree_1, ko_tree_2, ko_tree_3] = ko_tree_remove_leafs(ko_tree);

ind_level_1 = [];
ind_level_2 = [];
ind_level_3 = [];
ind_level_4 = [];

children_of_level_1 = {};
children_of_level_2 = {};
children_of_level_3 = {};

collect_level_2 = [];
collect_level_3 = [];
collect_level_4 = [];

for it = 1:length(ko_tree),
  if strcmp(ko_tree{it}(1:3),sprintf('\t\t\t'))
    ind_level_4     = [ind_level_4, it];
    collect_level_4 = [collect_level_4, it];
  elseif strcmp(ko_tree{it}(1:2),sprintf('\t\t')),
    ind_level_3 = [ind_level_3, it];
    collect_level_3 = [collect_level_3, it];
    children_of_level_3 = [children_of_level_3,collect_level_4];
    collect_level_4 = [];
  elseif strcmp(ko_tree{it}(1),sprintf('\t')),
    ind_level_2 = [ind_level_2, it];
    collect_level_2 = [collect_level_2, it];
    children_of_level_3 = [children_of_level_3,collect_level_4];
    collect_level_4 = [];
    children_of_level_2 = [children_of_level_2,collect_level_3];
    collect_level_3 = [];
  else
    ind_level_1     = [ind_level_1, it];
    children_of_level_3 = [children_of_level_3,collect_level_4];
    collect_level_4 = [];
    children_of_level_2 = [children_of_level_2,collect_level_3];
    collect_level_3 = [];
    children_of_level_1 = [children_of_level_1,collect_level_2];
    collect_level_2 = [];
  end
end

children_of_level_3 = [children_of_level_3,collect_level_4];
children_of_level_2 = [children_of_level_2,collect_level_3];
children_of_level_1 = [children_of_level_1,collect_level_2];


% ----------------------------------------------
% insert all given colors 

colors = nan * ones(length(ko_tree),3);

for it = 1:length(ind_level_2),
  ll = label_names({ko_tree{ind_level_2(it)}(2:end)},names);
  if ll,
    colors(ind_level_2(it),:) = col(ll,:);
  end
end


% ----------------------------------------------
% compute and insert all higher-level colors 
% (to fill missing colors later on)

for it = 1:length(ind_level_1),
  ind_missing = find(isnan(colors(children_of_level_1{it},1)));
  mean_color  = nanmean(colors(children_of_level_1{it},:));
  colors(ind_level_1(it),:) = mean_color;
  if ind_missing,
    colors(children_of_level_1{it}(ind_missing),:) = repmat(mean_color,length(ind_missing),1);
  end
end


display('Please wait a moment');


% ----------------------------------------------
% compute and insert all 3rd level colors

for it = 1:length(ind_level_2),
  mean_color   = colors(ind_level_2(it),:);
  ind_children = children_of_level_2{it};
  my_colors    = repmat(mean_color,length(ind_children),1);
  my_names     = ko_tree(ind_children);
  for itt = 1:size(my_colors,1),
    rng(sum(double(my_names{itt})),'v5uniform');
    dum = 2 * rand(1,3)-1; 
    my_colors(itt,:) = my_colors(itt,:) + 0.05 * dum /norm(dum);
    my_colors(itt,:) = exp(0.045*randn) * my_colors(itt,:); 
  end
  colors(ind_children,:) = my_colors;  
end


% ----------------------------------------------
% compute and insert all 4th level colors

for it = 1:length(ind_level_3),
  mean_color   = colors(ind_level_3(it),:);
  ind_children = children_of_level_3{it};
  my_colors    = repmat(mean_color,length(ind_children),1);
  my_names     = ko_tree(ind_children);
  for itt = 1:size(my_colors,1),
    rng(sum(double(my_names{itt})),'v5uniform');
    dum = 2 * rand(1,3)-1;
    my_colors(itt,:) = my_colors(itt,:) + 0.02 * dum/norm(dum);
    my_colors(itt,:) = exp(0.03*randn) * my_colors(itt,:); 
  end
  colors(ind_children,:) = my_colors;  
end

colors(colors<0) = 0; colors(colors>1) = 1;

figure(2); 
n_ko = 4700;
[ni,nk] = subplot_n(ceil(n_ko));
im(reshape(1:ni*nk,ni,nk),[1,n_ko])
colormap(colors); title('All levels');

figure(3); 
n_ko = 4700;
[ni,nk] = subplot_n(ceil(n_ko));
im(reshape(1:ni*nk,ni,nk),[1,n_ko])
colormap(colors(ind_level_4,:)); title('Only KO');

% -------------------------------------------
% add grey for "Not mapped" category and save colour table

V = colors(ind_level_4,:);

V = [V; 0.34 0.36 0.38];
ko_list = [ko_list; {'Not Mapped'}];

mytable([ko_list,num2cell(V(:,1)),num2cell(V(:,2)),num2cell(V(:,3))],0,[ data_directory '/hierarchy/KO_color_table.csv']);
