function join_protein_data_files(dir,files,samples,organism,outfile)

if 0,
  % Example

  dir = '/home/wolfram/projekte/proteomaps/github/proteomaps-workflow/data_original/valgepea_ecoli';
  files = {[dir '/eco_mu0.11_abundance.csv'] ...
           [dir '/eco_mu0.21_abundance.csv'] ...
           [dir '/eco_mu0.31_abundance.csv'] ...
           [dir '/eco_mu0.40_abundance.csv'] ...
           [dir '/eco_mu0.48_abundance.csv']};
  samples = {'mu_0_11', 'mu_0_21', 'mu_0_31', 'mu_0_40', 'mu_0_48'}';
  organism = 'eco';
  outfile ='/home/wolfram/projekte/proteomaps/github/proteomaps-workflow/proteomovies/examples/valgepea_ecoli/valgepea_ecoli.tsv';
  join_protein_data_files(dir,files,samples,organism,outfile)

end

% ---------------------------------------------------------------------------

T = {['!!SBtab TableType="Proteomaps" Organism="', organism, '"']; '!Gene'};

for it = 1:length(samples),
 T(2,1+it) = samples(it);
end

gene_names = [];
for it = 1:length(files),
  S{it} = load_any_table(files{it});
  ind_data_rows = find(cellfun('length', strfind(S{it}(:,1),'!'))==0);
  S{it} = S{it}(ind_data_rows,:);
  gene_names = [gene_names; S{it}(:,1)];
end

gene_names_unique = unique(gene_names);
data = zeros(length(gene_names_unique), length(samples));

for it = 1:length(files),
  ind = label_names(S{it}(:,1), gene_names_unique);
  data(ind,it) = cell_string2num(S{it}(:,2));
end

T = [T; [gene_names_unique, num2cell(data)]]; 

mytable(T,0,outfile);