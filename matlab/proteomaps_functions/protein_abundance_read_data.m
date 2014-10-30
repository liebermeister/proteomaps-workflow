% ----------------------------------------------------------------------
% read protein data and save them in .mat file
% requires directory name to be given in variable 'data_directory'

nnn = findstr('/', data_directory);
if nnn(end) == length(data_directory), nnn = nnn(1:end-1); end
data_sets = data_directory(nnn(end)+1:end);

if protein_lengths,
  outfile = [data_sets '_read_data_protein_lengths'];
else
  outfile = [data_sets '_read_data'];
end

A = load_any_table([data_directory '/filenames.csv']);

data_organisms   = A(:,1)';
data_filenames   = A(:,2)';
data_shortnames  = A(:,3)';
data_legendnames = A(:,4)';

% ind.spo      = find(strcmp('spo',data_organisms));
% ind.eco      = find(strcmp('eco',data_organisms));
% ind.sce      = find(strcmp('sce',data_organisms));
% ind.ath      = find(strcmp('ath',data_organisms));
% ind.hsa      = find(strcmp('hsa',data_organisms));
% ind.bacteria = ind.eco;
% ind.all      = 1:length(data_organisms);
ind = [];

if protein_lengths,
  for it = 1:length(data_filenames),
    lll = findstr('/',data_filenames{it}); lll = lll(end);
    data_filenames{it} = [data_directory '/' data_shortnames{it} '/' data_organisms{it} '_cost_' data_filenames{it}(lll+1:end)];
  end
end

for it = 1:length(data_shortnames),
  data.(data_shortnames{it}) = load_any_table(data_filenames{it});
  % remove lines starting with "!"
  ok = find(cellfun('length',strfind( data.(data_shortnames{it})(:,1) ,'!'))==0)
  data.(data_shortnames{it}) = data.(data_shortnames{it})(ok,:);
end

ko_tree = load_file_as_strings([data_directory '/hierarchy/KO_hierarchy_standardised.tms']);
ko_list = ko_tree_extract_ko_list(ko_tree);

protein_data = protein_abundance_read_data_once(data_organisms, data_shortnames, data_filenames, data_legendnames, data, ko_list,data_directory);

[cumulative_value,X,ko_tree_1,ko_tree_2,ko_tree_3] = protein_abundance_branch_ratios_cumulative(ko_tree,protein_data.ko_ids,protein_data.protein_numbers);


% --------------------------------------------------------
% table abundance ratios; division by 0 yields inf; division 0/0 yields nan

ll = label_names(ko_tree_2,ko_tree);
categories = strrep(ko_tree(ll),sprintf('\t'),'-');

ind_nonmapped = find(strcmp(upper('Not mapped'),upper(categories)));

M2 = [nansum(X); [nansum(X)-cumulative_value(ll(ind_nonmapped),:)]; cumulative_value(ll,:)];
categories = [{'TOTAL'; 'MAPPED'}; categories];

ratios = [];
for it = 1:size(M2,2),
  MM2 = M2(:,it) * [1./M2(:,it)'];
  MM2(find(M2(:,it)~=0),find(M2(:,it)==0)) = inf;
  ratios = [ratios MM2(:)];
end

ind_inf = find(isinf(ratios));
ratios = roundsd(ratios,4);
ratios(ind_inf) = inf;


% --------------------------------------------------------------
% randomised versions; division by 0 yields inf; division 0/0 yields nan

clear ratio_matrix_list

for itt = 1:n_randomised_trees,
  sprintf('Permutation sample %d/%d',itt,n_randomised_trees)
  my_ko_tree = load_file_as_strings(sprintf([SUBSAMPLED_TREE_DIR '/KO_hierarchy_standardised_multiple_occurance_%d.tms'],itt));
  [my_cumulative_value,my_X,my_ko_tree_1,my_ko_tree_2] = protein_abundance_branch_ratios_cumulative(my_ko_tree,protein_data.ko_ids,protein_data.protein_numbers);
   ll = label_names(my_ko_tree_2,my_ko_tree);
   my_categories = strrep(my_ko_tree(ll),sprintf('\t'),'-');
   my_ind_nonmapped = find(strcmp(upper('Not mapped'),upper(my_categories)));
   my_M2 = [nansum(my_X); [nansum(my_X)-my_cumulative_value(ll(my_ind_nonmapped),:)]; my_cumulative_value(ll,:)];
   my_categories = [{'TOTAL'; 'MAPPED'}; my_categories];
   my_ratios = [];
   for it = 1:size(my_M2,2),
     my_MM2 = my_M2(:,it) * [1./my_M2(:,it)'];
     my_MM2(find(my_M2(:,it)~=0),find(my_M2(:,it)==0)) = inf;
     my_ratios = [my_ratios my_MM2(:)];
   end
   ind_inf = find(isinf(my_ratios));
   my_ratios = roundsd(my_ratios,4);
   my_ratios(ind_inf) = inf;
   ratio_matrix_list(itt,:,:) = my_ratios;
end

ratio_matrix_10_percent = squeeze(quantile(ratio_matrix_list,0.1));
ratio_matrix_50_percent = squeeze(quantile(ratio_matrix_list,0.5));
ratio_matrix_90_percent = squeeze(quantile(ratio_matrix_list,0.9));


% --------------------------------------------------------
% table abundances of 3rd level categories

ll3 = label_names(ko_tree_3,ko_tree);
categories3 = strrep(ko_tree(ll3),sprintf('\t'),'-');

ind_nonmapped3 = find(strcmp(upper('Not mapped'),upper(categories3)));

M3 = [nansum(X); [nansum(X)-cumulative_value(ll3(ind_nonmapped3),:)]; cumulative_value(ll3,:)];
categories3 = [{'TOTAL'; 'MAPPED'}; categories3];


%-------------------------------------------------------

cd(PROTEOMAPS_MATLAB_DATA_DIR);

save(outfile,'protein_data','ind', 'ko_tree', 'ko_list','n_randomised_trees','cumulative_value','X','ko_tree_1','ko_tree_2','ko_tree_3','ratios','ratio_matrix_list','ratio_matrix_10_percent','ratio_matrix_50_percent','ratio_matrix_90_percent','categories','my_categories','M3','categories3');
