function treemap_plot(levels,names,rects,colors,options)

eval(default('options','struct'));
options_default = struct('show_text',1,'shift_text',1,'fontsize',6,'show_level',2);
options = join_struct(options_default,options);

hold on; 

% draw colored rectangles

for it = 1:length(names),
  if levels(it) == 4,
    rect = rects(it,:);
    fill([rect(1),rect(2),rect(2),rect(1)], [rect(3),rect(3),rect(4),rect(4)],colors(it,:),'EdgeColor',[.2 .2 .2]); 
  end
end

% draw borders

for it = 1:length(names),
  rect = rects(it,:);
  switch levels(it),
    case 1,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'k-','LineWidth',1); 
    case 2,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'k-','LineWidth',1); 
    case 3,
      plot([rect(1),rect(2),rect(2),rect(1),rect(1)], [rect(3),rect(3),rect(4),rect(4),rect(3)],'-','Color',[.1 .1 .1]); 
  end
end

% show text

if options.show_text,
for it = 1:length(names),
  switch levels(it),
    case options.show_level,
      rect = rects(it,:);
      if options.shift_text,
        alpha = 0.4 + 0.2 * rand;
      else
        alpha = 0.5;
      end
      text(0.95*rect(1)+0.05*rect(2),alpha* rect(3)+(1-alpha)* rect(4),names(it),'FontWeight','bold','FontSize',options.fontsize,'Color',[1 1 1]);  % break_names(names(it)),
  end
end
end

hold off; axis off; axis square
