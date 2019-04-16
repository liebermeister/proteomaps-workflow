function my_tree = ko_tree_replace_labels(ko_tree, ko_labels,replace_labels)

for it = 1:length(ko_tree),
  if strcmp(sprintf('\t\t\t'), ko_tree{it}(1:3)),
    my_ko = ko_tree{it}(4:end);
    ll = find(strcmp(my_ko,ko_labels));
    if ll,
      my_tree{it,1} = sprintf('\t\t\t%s',replace_labels{ll(1)});
    else
      my_tree{it,1} = sprintf('\t\t\t%s',my_ko);
    end
  else
   my_tree{it,1} = ko_tree(it);
  end
end
