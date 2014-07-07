function ko_tree = ko_tree_select_ko(KO_tree,my_ko)

ko_tree = {};
for it = 1:length(KO_tree)
  if strcmp(sprintf('\t\t\t'),KO_tree{it}(1:3)),
    if find(strcmp(KO_tree{it}(4:end),my_ko)),
      ko_tree = [ko_tree; KO_tree{it}];
    end
  else
    ko_tree = [ko_tree; KO_tree{it}];
  end
end

ko_tree = ko_tree_omit_unused(ko_tree);
