function protein_data = protein_abundance_read_data_once( data_organisms, data_shortnames, data_filenames, data_legendnames, data, ko_list, data_directory, verbose)

eval(default('verbose','0'));

% --------------------------------------------------------------
% map and put together data

protein_numbers = [];

for it = 1:length(data_shortnames),
  if verbose, display(data_shortnames{it}); end
  mapping_table = load_any_table([data_directory '/hierarchy/' data_organisms{it} '_mapping_standardised_pair.csv']);
  %% my_syst_names: all syst names in the dataset
  %% my_ko_numbers: all corresponding ko numbers
  %% my_values:     all corresponding ko numbers
  my_syst_names = data.(data_shortnames{it})(:,1); 
  ll = label_names(my_syst_names,mapping_table(:,2));
  my_ko_numbers                = {};
  my_ko_numbers(find(ll),1)    = mapping_table(ll(find(ll)),1);
  my_ko_numbers(find(ll==0),1) = repmat({'NotMapped'},sum(ll==0),1);
  
  my_protein_numbers = nan * ones(size(ko_list));
  my_values          = cell_string2num(data.(data_shortnames{it})(:,2));
  %% my_mapped_values: values only for genes that have a KO number
  %% my_mapped_values = cell_string2num(data.(data_shortnames{it})(find(ll),2));
  ll = label_names(ko_list,my_ko_numbers,'multiple');
  %% sum over all genes with the same ko number
  for itt = 1:length(ko_list),  
    if ll{itt}, my_protein_numbers(itt) = nansum(my_values(ll{itt})); end; 
  end
  protein_numbers = [protein_numbers, my_protein_numbers];
end

n_genes = length(ko_list);
protein_numbers(protein_numbers==0) = 0.1*min(protein_numbers(protein_numbers~=0));

% # proteins mapped for each per data set
if verbose,
  print_matrix(sum(isfinite(protein_numbers))',data_shortnames, [])
end

% how many ko numbers are found in no data set?  
% -> in case of problems, maybe  extract_relevant_ko.py contained wrong filenames
if verbose,
  length(find(sum(isfinite(protein_numbers),2) ==0))
end

protein_data.ko_ids           = ko_list;
protein_data.data_sets        = data_filenames';
protein_data.data_sets_short  = strrep(data_shortnames,'_',' ')' ;
protein_data.data_sets_legend = column(data_legendnames);
protein_data.organisms        = data_organisms' ;
protein_data.protein_numbers  = protein_numbers;
