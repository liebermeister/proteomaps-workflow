function ko_tree = ko_tree_shift_one_level_up(ko_tree)

% remove the top-level node and shift all nodes one level up

ko_tree = ko_tree(2:end);

for it = 1:length(ko_tree),
  ko_tree{it} = ko_tree{it}(2:end);
end
