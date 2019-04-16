function summed_sizes = tree_sizes(levels,sizes)

summed_sizes   = sizes;
old_level      = levels(end);
collected_size = zeros(1,10);

for it = length(levels):-1:1,
  my_level = levels(it);
  my_size  = sizes(it);
  if my_level == old_level,
    collected_size(my_level) = collected_size(my_level) + my_size;
  end
  if my_level > old_level,
    collected_size(my_level) = my_size;
    if old_level>1,
      collected_size(old_level-1) = collected_size(old_level);    
    end
    collected_size(old_level)   = 0;
  end
  if my_level < old_level,
    collected_size(my_level) = collected_size(my_level) + collected_size(old_level);
    collected_size(my_level+1:end) = 0;
    summed_sizes(it) = collected_size(my_level);
  end  
  old_level = my_level;
end