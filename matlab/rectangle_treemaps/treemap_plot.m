function treemap_plot(levels,names,rects,colors,show_names,options)

eval(default('options','struct','show_names','names'));
options_default = struct('show_text',1,'shift_text',1,'fontsize',6,'show_level',2,'strong_lines',1,'sample_label',[],'protein_minimal_size_for_label',0.001,'fontcolor',[1 1 1]);
options = join_struct(options_default,options);

hold on; 

% draw colored rectangles

for it = 1:length(names),
  if levels(it) == max(levels),
    rect = rects(it,:);
    fill([rect(1),rect(2),rect(2),rect(1)], [rect(3),rect(3),rect(4),rect(4)],colors(it,:),'EdgeColor',[.2 .2 .2]); 
  end
end

% draw borders

if options.strong_lines, 
  lw = 2;
else
  lw = 1;
end

for it = 1:length(names),
  rect = rects(it,:);
  switch levels(it),
    case 1,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'k-','LineWidth',1); 
    case 2,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'k-','LineWidth',1); 
    case 3,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'-','Color',[.1 .1 .1],'LineWidth',lw); 
  end
end

% show labels

if options.show_text,
  if options.shift_text,
    alpha = 0.4 + 0.2 * rand;
  else
    alpha = 0.5;
  end
  for it = 1:length(names),
    if levels(it) == options.show_level,
      rect = rects(it,:);
      % show label or not?
      if levels(it) == 4,
        ok = [rect(2) - rect(1)] * [rect(4) - rect(3)] > options.protein_minimal_size_for_label;
      else
        ok = 1;
      end
      if ok,
        my_fontsize = ceil([0.8 + 4 * [rect(2) - rect(1)] * [rect(4) - rect(3)]] * options.fontsize);
        beta = 0.5 * tanh( [rect(2) - rect(1)] / [my_fontsize/20 * length(names(it))] );
        my_x = (1-beta) * rect(1) + beta * rect(2);
        my_y = alpha* rect(3)+(1-alpha)* rect(4);
        text(my_x,my_y,show_names(it),'FontWeight','bold','FontSize',my_fontsize,'Color',options.fontcolor);
        %% break_names(names(it)),
      end
    end
  end
end

if length(options.sample_label),
  text(0.01,0.01,options.sample_label,'FontSize',16);
end

hold off; axis off; axis square
