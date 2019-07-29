function [cumulative_value,X,ko_tree_1,ko_tree_2,ko_tree_3] = protein_abundance_branch_ratios_cumulative(ko_tree,ko_ids,protein_numbers)

% cumulative_value: cumulative abundance values for categories (rows, as listed in ko_tree)
% X: single KO abundance numbers (proteins in rows, as listed by ko_ids)

% ----------------------------------------------------------------
% compute cumulative values in tree

[ko_tree_1, ko_tree_2, ko_tree_3] = ko_tree_remove_leafs(ko_tree);
X = protein_numbers;
X(isnan(X)) = 0;

old_level  = 3;
old_sum(3,:) = zeros(1,size(X,2));
old_sum(2,:) = zeros(1,size(X,2));
old_sum(1,:) = zeros(1,size(X,2));

for it = length(ko_tree):-1:1,
  level = length(findstr(ko_tree{it},sprintf('\t')));
  if level == 0,
    cumulative_value(it,:) = old_sum(1,:);
    old_sum(1,:) = zeros(1,size(X,2));;
  elseif level == 1,
    cumulative_value(it,:) = old_sum(2,:);
    old_sum(2,:) = zeros(1,size(X,2));;
  elseif level == 2,
    cumulative_value(it,:) = old_sum(3,:);
    old_sum(3,:) = zeros(1,size(X,2));;
  elseif level == 3,
    ii = find(strcmp(ko_tree{it}(4:end),ko_ids));
    if length(ii),
      cumulative_value(it,:) = X(ii,:);
      if old_level < 3,
        old_sum(3,:) = zeros(1,size(X,2));
      end
      old_sum(1,:) = old_sum(1,:) + X(ii,:);
      old_sum(2,:) = old_sum(2,:) + X(ii,:);
      old_sum(3,:) = old_sum(3,:) + X(ii,:);
    end
  end
  old_level = level;
end
