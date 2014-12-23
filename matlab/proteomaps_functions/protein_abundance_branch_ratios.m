% requires variables: 
%  'data_directory' directory name
%  'data_sets' name of data set bundle
%  'protein_lengths' (Boolean)

if 0,
%  data_sets       = 'protein_abundances_paper';
  data_directory  = ['/home/wolfram/projekte/protein_abundance/proteomaps_data_sets/' data_sets '/'];
  protein_lengths = 0;
end

eval(['! mkdir ' data_directory '/tables']);

switch protein_lengths,
  case 0,
    infile   = [data_sets '_read_data'];
    filename = [data_directory '/tables/category_abundance'];
    filename_ko = [data_directory '/tables/ko_abundance.csv'];
  case 1,
    infile   = [data_sets '_read_data_protein_lengths'];
    filename = [data_directory '/tables/category_cost'];
    filename_ko = [data_directory '/tables/ko_cost.csv'];
end

% load preprocessed data from protein_abundance_read_data.m

proteomaps_path_names;
load([PROTEOMAPS_MATLAB_DATA_DIR '/' infile]);

% --------------------------------------------------------
% save table with all proteome data, aligned by KO

my_numbers = protein_data.protein_numbers; 
mytable([{'KO number'},protein_data.data_sets_short'; protein_data.ko_ids, num2cell(my_numbers)],0,filename_ko);

% --------------------------------------------------------
% display cumulative values 

% 1st and 2nd hierarchy level as matrix

figure(1);
ll = label_names(ko_tree_2,ko_tree);
M  = cumulative_value(ll,:) * diag(1./nansum(X));
im(M,[],ko_tree_2,protein_data.data_sets_short);

% 1st hierarchy level as bar plot

n_data_sets = length(protein_data.data_sets);

figure(2);
ll = label_names(ko_tree_1,ko_tree);
M = cumulative_value(ll,:) * diag(1./nansum(X));
bar(M','stacked'); colormap(ryb_colors); axis tight; legend(ko_tree_1,'Fontsize',6,'Location','SouthWest')
set(gca,'YTick',[],'XTickLabel',protein_data.data_sets_legend); my_xticklabel(1:n_data_sets,-0.1);


% ----------------------------------------------------------------------
% 2nd hierarchy level as bar plot and pie plot

ll = setdiff(label_names(ko_tree_2,ko_tree),label_names(ko_tree_1,ko_tree));
second_order_names =  strrep(ko_tree(ll),sprintf('\t'),'');
M = cumulative_value(ll,:) * diag(1./nansum(X));

% omit small categories from the barplot 
ind_show = find(sum(M,2)>0.01);
M = M(ind_show,:); 
M = M * diag(1./nansum(M));
second_order_names = second_order_names(ind_show);

% load colours
A = load_any_table([PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv']);
%A = load_any_table('~/projekte/protein_abundance/data/Protein_category_colours_Dark.csv');
lll = label_names(second_order_names,A(:,1)); 
if find(lll==0), 
  second_order_names(find(lll==0))
  error('Category missing in colour list'); 
end
protein_colors = cell_string2num(A(lll(find(lll)),2:end));

figure(3); clf
subplot('Position',[0.02 0.05 0.95 0.8]); 
h = bar(M','stacked'); colormap(protein_colors); axis tight;
legend(fliplr(h),flipud(second_order_names),'Fontsize',7,'Location','EastOutside')
set(gca,'YTick',[],'XTickLabel',protein_data.data_sets_legend); my_xticklabel(1:n_data_sets,0.06);

for it =1:length(protein_data.data_sets),
  figure(500+it); clf
  my_ind = find(M(:,it));
  pie(M(my_ind,it),second_order_names(my_ind)); colormap(protein_colors(my_ind,:))
  title(protein_data.data_sets_legend{it})
end


% --------------------------------------------------------
% table abundance ratios for avi

category_labels = [ repmat(categories,length(categories),1), ...
                    reshape(repmat(categories',length(categories),1),length(categories)^2,1)];

protein_data.data_sets_short = column(protein_data.data_sets_short);

mytable([[{'Numerator','Denominator'},protein_data.data_sets_short']; [category_labels, num2cell(ratios)]],0,[ filename '_ratios.csv']);


% --------------------------------------------------------------
% randomised versions

category_labels = [ repmat(my_categories,length(my_categories),1), ...
                    reshape(repmat(my_categories',length(my_categories),1),length(my_categories)^2,1)];

if size(ratio_matrix_10_percent,1) ==1;
  ratio_matrix_10_percent = ratio_matrix_10_percent';
  ratio_matrix_50_percent = ratio_matrix_50_percent';
  ratio_matrix_90_percent = ratio_matrix_90_percent';
end

mytable([{'Numerator','Denominator'},protein_data.data_sets_short'; category_labels, num2cell(ratio_matrix_10_percent)],0,[filename '_ratios_10.csv']);

mytable([{'Numerator','Denominator'},protein_data.data_sets_short'; category_labels, num2cell(ratio_matrix_50_percent)],0,[filename '_ratios_50.csv']);

mytable([{'Numerator','Denominator'},protein_data.data_sets_short'; category_labels,num2cell(ratio_matrix_90_percent)],0,[filename '_ratios_90.csv']);

ns = length(protein_data.data_sets_short);
nc = size(ratio_matrix_10_percent,1);
mytable([{'Numerator','Denominator'},reshape(repmat(protein_data.data_sets_short,3,1),3*ns,1)'; ...
       [{'',''},repmat({'10%','50%','90%'},1,ns)]; ...
       [category_labels, num2cell(reshape([ratio_matrix_10_percent; ratio_matrix_50_percent; ratio_matrix_90_percent],nc,3*ns))]],0,[filename '_ratios_quantiles.csv']);


% --------------------------------------------------------------
% tables with 3rd level categories

mytable([{'Category'},protein_data.data_sets_short'; categories3, num2cell(M3 * diag(1./M3(1,:)))],0,[filename '.csv']);
%absolute numbers
%mytable([{'Category'},protein_data.data_sets_short'; categories3, num2cell(M3)],0,[filename '.csv'])


% --------------------------------------------------------------
figure(10);
subplot(1,3,1); im(log10(ratio_matrix_10_percent),[-10,10]);
subplot(1,3,2); im(log10(ratio_matrix_50_percent),[-10,10]);
subplot(1,3,3); im(log10(ratio_matrix_90_percent),[-10,10]);

% --------------------------------------------------------------
% bar plot with median values

ind  = find(strcmp('TOTAL',category_labels(:,2)));
ind2 = find(cellfun('length',strfind(category_labels(ind,1),'-')));
ind = ind(ind2);
ratio_matrix_50_percent_level_2 = ratio_matrix_50_percent(ind,:);
category_labels_level_2 = category_labels(ind,1);
category_labels_level_2 = strrep(category_labels_level_2,'-','');

% omit small categories from the barplot 
ind_show = find(sum(ratio_matrix_50_percent_level_2,2)>0.01);
ratio_matrix_50_percent_level_2 = ratio_matrix_50_percent_level_2(ind_show,:); 
ratio_matrix_50_percent_level_2 = ratio_matrix_50_percent_level_2 * diag(1./nansum(ratio_matrix_50_percent_level_2));
category_labels_level_2 = category_labels_level_2(ind_show);

% load colours
A = load_any_table([PROTEOMAPS_RESOURCE_DIR '/KO_gene_hierarchy_colors.csv']);
lll = label_names(category_labels_level_2,A(:,1)); 
protein_colors = cell_string2num(A(lll(find(lll)),2:end));

figure(11); clf
subplot('Position',[0.02 0.05 0.95 0.8]); 
h = bar(ratio_matrix_50_percent_level_2','stacked'); colormap(protein_colors); axis tight;
legend(fliplr(h),flipud(category_labels_level_2),'Fontsize',7,'Location','EastOutside')
set(gca,'YTick',[],'XTickLabel',protein_data.data_sets_legend); my_xticklabel(1:n_data_sets,0.06);


% ----------------------------------------------------------

cd ~/projekte/protein_abundance/ps-files/numbers_in_categories/

if protein_lengths,
  print([ data_sets '_protein_cost_in_categories_matrix.eps'], '-f1', '-depsc');
  print([ data_sets '_protein_cost_in_categories_level1.eps'], '-f2', '-depsc');
  print([ data_sets '_protein_cost_in_categories_level2.eps'], '-f3', '-depsc');
  print([ data_sets '_protein_cost_in_categories_level2_median.eps'], '-f11', '-depsc');
  for it =1:length(protein_data.data_sets),
    print([ data_sets '_' strrep(protein_data.data_sets_short{it},' ','_') '_protein_cost_in_categories_level2_pie.eps'], ['-f' num2str(500+it)], '-depsc');
  end
else
  print([ data_sets '_abundance_in_categories_matrix.eps'], '-f1', '-depsc');
  print([ data_sets '_abundance_in_categories_level1.eps'], '-f2', '-depsc');
  print([ data_sets '_abundance_in_categories_level2.eps'], '-f3', '-depsc');
  print([ data_sets '_abundance_in_categories_level2_median.eps'], '-f11', '-depsc');
  for it =1:length(protein_data.data_sets),
    print([ data_sets  '_' strrep(protein_data.data_sets_short{it},' ','_') '_protein_abundance_in_categories_level2_pie.eps'], ['-f' num2str(500+it)], '-depsc');
  end
end



% --------------------------------------------------------------
% individual tables with relative abundances for each data set and each level

clear data_set_short
for it = 1:length(protein_data.data_sets_short)
  data_set_short{it} = strrep(protein_data.data_sets_short{it},' ','_');
end

ko_level_1 = ko_tree_1;
ko_level_2 = setdiff(ko_tree_2,ko_tree_1);
ko_level_3 = setdiff(ko_tree_3,ko_tree_2);

% relative amounts level 1
ll1 = label_names(ko_level_1,ko_tree);
M1 = cumulative_value(ll1,:) * diag(1./nansum(X));
% relative amounts level 2
ll2 = label_names(ko_level_2,ko_tree);
M2 = cumulative_value(ll2,:) * diag(1./nansum(X));
% relative amounts level 3
ll3 = label_names(ko_level_3,ko_tree);
M3 = cumulative_value(ll3,:) * diag(1./nansum(X));


for it = 1:length(protein_data.data_sets_short)

  dd = protein_data.data_sets{it}; ff = findstr(dd,'/'); dd = dd(ff(end)+1:end);
  dd = strrep(dd,'.txt','.csv');
  dd = strrep(dd,'.csv','.csv');
  dd = strrep(dd,[protein_data.organisms{it} '_cost_'],'');
  basename = [data_directory '/' data_set_short{it} '/'];
  filename_in = [basename data_set_short{it} '.csv'];
  T = load_any_table(filename_in);

  switch protein_lengths,
    case 0,
      all_values = cell_string2num(T(2:end,3));
      filename_for_html = [basename data_set_short{it} '_abundance_relative'];
    case 1,
      all_values = cell_string2num(T(2:end,5));
      filename_for_html = [basename data_set_short{it} '_cost_relative'];
  end
  
  % Level 5
  

  % If genes occur multiple times, sum over their values
  if length(unique(T(:,1))) ~= length(T(:,1)),
    warning(sprintf('Multiply occuring gene names in data set %s',protein_data.data_sets_short{it}));
    all_gene_names = T(2:end,1);
    unique_gene_names = unique(all_gene_names);
    ind = label_names(unique_gene_names, all_gene_names, 'multiple');
    TT = {};
    for itt = 1:length(ind),
      TT{itt,1} = unique_gene_names{itt};
      TT{itt,2} = 10^-6 * sum(all_values(ind{itt}));
    end
    mytable(TT,0, [filename_for_html '_lv5.csv']);
  else
    % otherwise simply write down data from input table
    mytable([T(2:end,1), num2cell(10^-6 * all_values)],0, [filename_for_html '_lv5.csv']);
  end

  % Levels 1, 2, and 3
  
  mytable([ko_level_1,num2cell(M1(:,it))],0,                             [filename_for_html '_lv1.csv']);
  mytable([strrep(ko_level_2,sprintf('\t'),''),num2cell(M2(:,it))],0,    [filename_for_html '_lv2.csv']);
  mytable([strrep(ko_level_3,sprintf('\t'),''),num2cell(M3(:,it))],0,    [filename_for_html '_lv3.csv']);

end
