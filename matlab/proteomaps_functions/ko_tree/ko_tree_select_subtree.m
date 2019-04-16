function [kko_tree,ko_list] = ko_tree_select_subtree(ko_tree,subtree_name)

it = 1; 
while ~length(strfind(ko_tree{it},subtree_name)),
  it=it+1;
end
level = length(strfind(ko_tree{it},sprintf('\t')));

kko_tree = ko_tree(it);
it=it+1;
my_level = 10;
while my_level>level,
kko_tree = [kko_tree;  ko_tree(it)];
it = it+1;
my_level = length(strfind(ko_tree{it},sprintf('\t')));
end

ko_list = ko_tree_extract_ko_list(kko_tree);
