function ko_list = ko_tree_extract_ko_list(ko_tree)

ko_list = {};
for it = 1:length(ko_tree),
  if length(ko_tree{it})>3,
    if strcmp(ko_tree{it}(1:3),sprintf('\t\t\t')),
      ko_list = [ko_list; ko_tree{it}(4:end)];
    end
  end
end
