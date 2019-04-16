function rects = treemap_flat(rect,names,sizes,colors,split_direction,fixed_arrangement)

if length(names) < 2, 

  rects = rect;

else,

  if fixed_arrangement,
    %% by counts (needed for reproducible arrangement)
    ind_split = ceil(length(names)/2);
  else,
    %% by area
    cumsum(sizes)/sum(sizes);
    ind_split = max( sum(cumsum(sizes)/sum(sizes)<=0.5),1);
  end
  
  names_1 = names(1:ind_split);
  names_2 = names(ind_split+1:end);
  sizes_1 = sizes(1:ind_split);
  sizes_2 = sizes(ind_split+1:end);
  colors_1 = colors(1:ind_split,:);
  colors_2 = colors(ind_split+1:end,:);
  r1 = sum(sizes_1)/sum(sizes);
  r2 = sum(sizes_2)/sum(sizes);
  
  switch split_direction,
    case 'flexible',
      if rect(2)-rect(1) > rect(4)-rect(3),
        do_split = 'vertical';
      else,      
        do_split = 'horizontal';
      end
    case 'horizontal',
      split_direction = 'vertical';
      do_split = 'vertical';
    case 'vertical',
      split_direction = 'horizontal';
      do_split =  'horizontal';
  end
  
  switch do_split,
    case 'horizontal',
      rect_1 = [rect(1), rect(2), rect(3) + r2*[rect(4)-rect(3)], rect(4)]; 
      rect_2 = [rect(1), rect(2), rect(3), rect(3) + r2 * [rect(4)-rect(3)]]; 
    case 'vertical',
      rect_1 = [rect(1), rect(1) + r1*[rect(2)-rect(1)], rect(3), rect(4)  ]; 
      rect_2 = [rect(1) + r1*[rect(2)-rect(1)], rect(2)  , rect(3), rect(4)  ]; 
  end
  
  rects_1 =  treemap_flat(rect_1,names_1,sizes_1,colors_1,split_direction,fixed_arrangement);
  rects_2 =  treemap_flat(rect_2,names_2,sizes_2,colors_2,split_direction,fixed_arrangement);
  rects = [rects_1; rects_2];
end
