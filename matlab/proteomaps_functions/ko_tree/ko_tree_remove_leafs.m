function [ko_tree_1, ko_tree_2, ko_tree_3] = ko_tree_remove_leafs(ko_tree)

% [ko_tree_1, ko_tree_2, ko_tree_3] = ko_tree_remove_leafs(ko_tree)

ko_tree_3 = ko_tree(find(cellfun('length',strfind(ko_tree,sprintf('\t\t\t')))==0));
ko_tree_2 = ko_tree_3(find(cellfun('length',strfind(ko_tree_3,sprintf('\t\t')))==0));
ko_tree_1 = ko_tree_2(find(cellfun('length',strfind(ko_tree_2,sprintf('\t')))==0));
