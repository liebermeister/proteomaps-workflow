function [kko_tree,ind_keep_lines] = ko_tree_remove_branch(ko_tree,branch)

lv  = get_level(branch);
ind = find(strcmp(ko_tree,branch));

if ind,
  it = ind+1;
  while [it<length(ko_tree)] * [get_level(ko_tree{it}) > lv],
    it = it+1;
  end
  if it<length(ko_tree), it=it-1; end
  ind_keep_lines = setdiff(1:length(ko_tree),ind:it);
else
  ind_keep_lines = 1:length(ko_tree); 
end
kko_tree = ko_tree(ind_keep_lines); 

function lv = get_level(my_string)

lv = 0;
if strcmp(my_string(1),sprintf('\t')),       lv = 1; end
if strcmp(my_string(1:2),sprintf('\t\t')),   lv = 2; end
if strcmp(my_string(1:3),sprintf('\t\t\t')), lv = 3; end
