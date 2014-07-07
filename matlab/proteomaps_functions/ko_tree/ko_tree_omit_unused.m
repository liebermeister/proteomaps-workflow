function ko_tree_out = ko_tree_omit_unused(ko_tree);

% remove lines in ko_tree that have no subelements

level = [];
for it = 1:length(ko_tree)
  this_line = ko_tree{it}; 
  if strcmp(sprintf('\t\t\t'),this_line(1:3)), level(it)=4; 
  elseif strcmp(sprintf('\t\t'),this_line(1:2)), level(it)=3; 
  elseif strcmp(sprintf('\t'),this_line(1)), level(it)=2; 
  else level(it)=1; 
  end
end

level(it+1) = 1;
ok(it+1) = 0;
for it = length(ko_tree):-1:1,
  ok(it) = [level(it) == 4] + ok(it+1) * [level(it+1) > level(it)];
end

ko_tree_out = ko_tree(find(ok));
