function [names,summed_sizes,colors,levels,show_names] = treemap_prepare_data(names,levels,summed_sizes,colortable,show_names)

eval(default('show_names','names'));

%% set color table
ind_colors = label_names(names,colortable.names);
colors     = ones(length(names),3);
colors(find(ind_colors),:) = colortable.colors(ind_colors(find(ind_colors)),:);

%% remove entries with zero cell size
ind_present  = find(summed_sizes>0);
names        = names(ind_present);         
levels       = levels(ind_present);       
summed_sizes = summed_sizes(ind_present); 
colors       = colors(ind_present,:);       
show_names   = show_names(ind_present);