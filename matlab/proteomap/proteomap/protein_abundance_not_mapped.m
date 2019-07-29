% ----------------------------------------------------------------------
% read protein data and display the highest-ranking proteins that are not mapped
% requires directory name to be given in variable 'data_directory'

A = load_any_table([data_directory '/filenames.csv']);

data_organisms  = A(:,1)';
data_filenames  = A(:,2)';
data_shortnames = A(:,3)';

ind.mpn      = find(strcmp('mpn',data_organisms));
ind.eco      = find(strcmp('eco',data_organisms));
ind.sce      = find(strcmp('sce',data_organisms));
ind.hsa      = find(strcmp('hsa',data_organisms));
ind.bacteria = ind.eco;
ind.all      = 1:length(data_organisms);

for it = 1:length(data_shortnames),
  display(data_shortnames{it})
  data.(data_shortnames{it}) = load_any_table(data_filenames{it});
  dd = data_filenames{it}; aaa = findstr('/',dd); dd = dd(aaa(end)+1:end);
  mapping_table_file = [ data_directory '/' data_shortnames{it} '/' data_shortnames{it} '_non_mapped.csv'];
  mapping_table = load_any_table(  mapping_table_file);
  all_syst_names = data.(data_shortnames{it})(:,1);
  ll = label_names(all_syst_names,mapping_table(:,2));
  my_syst_names = all_syst_names(find(ll));
  values = cell_string2num(data.(data_shortnames{it})(:,2));
  my_values = values(find(ll));
  value_sum = sum(values);
  [dum,order] = sort(-my_values);
  display(sprintf('not mapped: %f',sum(my_values)/value_sum))  
  display(print_matrix(my_values(order(1:10))/value_sum,my_syst_names(order(1:10))))
end
