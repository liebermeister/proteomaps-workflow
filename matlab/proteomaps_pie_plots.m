if 0,
  
  %% E coli
  data_file    = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_paper/eco_Lu/eco_abundance_table_protein_data_E_coli_Lu_1.csv';
  ps_file_pie      = 'pie_chart_eco_Lu';
  ps_file_bar      = 'bar_chart_eco_Lu';
  title_string = 'E. coli proteome (Lu et al. 2006)';
 colour_file = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_paper/hierarchy/KO_colour_table.csv';

 %% H sapiens
 data_file    = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_paper/hsa_Nagaraj/hsa_abundance_table_msb201181-s2_final_GluC.csv';
 ps_file_pie      = 'pie_chart_hsa_Nagaraj';
 ps_file_bar      = 'bar_chart_hsa_Nagaraj';
 title_string = 'Human cell line proteome (Nagaraj et al. 2011)';
 colour_file = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_paper/hierarchy/KO_colour_table.csv';

  %% S cerevisiae
 data_file    = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_other/sce_Nagaraj/sce_abundance_table_sce_nagaraj.csv';
 ps_file_pie      = 'pie_chart_sce_Nagaraj';
 ps_file_bar      = 'bar_chart_sce_Nagaraj';
 title_string = 'Yeast proteome (Nagaraj et al. 2012)';
 colour_file = '/home/wolfram/projekte/protein_abundance/data/protein_abundances_other/hierarchy/KO_colour_table.csv';
 
end


% -------------------------------------------------------------

C = load_any_table(colour_file);

color_table.KO = C(:,1);
color_table.colors = cell_string2num(C(:,2:end));

D = load_any_table(data_file);

data.KO    = D(2:end,8);
data.gene  = D(2:end,7);
data.value = cell_string2num(D(2:end,4));

show = struct;
show.genes = {};
show.color = [];
show.value = [];

for it = 1:length(color_table.KO),
 my_KO     = color_table.KO{it};
 my_color  = color_table.colors(it,:);
 my_ind    = find(strcmp(my_KO,data.KO));
 my_ind    = my_ind(data.value(my_ind)>0);
 my_genes  = data.gene(my_ind);
 my_values = data.value(my_ind);
 show.genes = [show.genes; column(my_genes)];
 show.color = [show.color; repmat(my_color,length(my_ind),1)];
 show.value = [show.value; column(my_values)];
end

show.some_genes = show.genes;
dum = sort(show.value); 
thr = dum(end-14);
ind_omit = find(show.value < thr);
show.some_genes(ind_omit) = repmat({''},length(ind_omit),1);

% figure(1);
% h = pie(show.value,show.some_genes);
% colormap(show.color);
% title(title_string)

figure(2); clf
bar([show.value(1:end)'; show.value(1:end)'],'stacked'); axis tight
colormap(show.color);
%title(title_string)
for it = 1:length(show.value),
  if length(show.some_genes{it}),
    text(1.42,sum(show.value(1:it-1))+0.5*show.value(it),show.some_genes{it},'Fontsize',12)
  end
end
axis off

cd ~/projekte/protein_abundance/ps-files/pie_charts
exportfig(1, ps_file_pie,'Color','rgb');
exportfig(2, ps_file_bar,'Color','rgb');

% umwandeln nach png in gimp:
% fuer pie chart import in gimp mit 500dpi, fuer bar chart 200 dpi; 
% jeweils starke glättung von text und linien