clear

rect_all = [0 1 0 1]; % left right bottom top

names  = {'A','B','C','D','E','F','G','H' 'I','A','B','C','D','E','F','G','H' 'I'}';
levels = [1   2    3   4   1   2    3    4   4 1   2    3    4   1   2   3   4   4 ];
sizes  = [nan nan  nan 1  nan  nan  nan  2   3 nan nan  nan  1 nan  nan  nan  2   3 ]';
colors = rb_colors(length(sizes));
split_direction = 'flexible';

summed_sizes = tree_sizes(levels,sizes);
rects        = treemap_hierarchical(rect_all,names,summed_sizes,colors,levels,split_direction);

figure(1); clf; 
treemap_plot(levels,names,rects,colors);
