function rects = treemap_hierarchical(rect,names,summed_sizes,colors,levels,split_direction,fixed_arrangement)


if length(unique(levels)) == 1,
  % if all items are on the same level:
  rects = treemap_flat(rect,names,summed_sizes,colors,split_direction,fixed_arrangement);

else
  %% otherwise, find highest-level items, compute their rectangles,
  %% then recursively run the function for each of them

  rects = [];

  min_level     = min(levels);
  ind_min_level = column(find([levels ==min_level]));

  switch split_direction,
    case 'horizontal',
      split_direction = 'vertical';
    case 'vertical',
      split_direction = 'horizontal';
   end
  
  my_rects = treemap_flat(rect,names(ind_min_level),summed_sizes(ind_min_level),colors(ind_min_level,:),split_direction,fixed_arrangement);
  
  rects(ind_min_level,:) = my_rects;
  
  ind_min_level = [ind_min_level; length(levels)+1];

  for it = 1:length(ind_min_level)-1,
    sub_indices = ind_min_level(it)+1:ind_min_level(it+1)-1;
    sub_levels  = levels(sub_indices);
    sub_sizes   = summed_sizes(sub_indices);  
    sub_names   = names(sub_indices);
    sub_colors  = colors(sub_indices,:);
    sub_rects   = treemap_hierarchical(my_rects(it,:),sub_names,sub_sizes,sub_colors,sub_levels,split_direction,fixed_arrangement);
    rects(sub_indices,:) = sub_rects;    
  end
  
end

