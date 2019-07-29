function movie_save(filename, M, my_delay, duration)

% movie_save(filename, M, my_delay, duration)
%
% M movie object
% my_delay is in 1/100 seconds
% duration (in seconds) overrides my_delay

eval(default('my_delay','[]','resolution','30','duration','[]'));

[fpath,fname,fext] = fileparts(filename);

fname = [fname fext];

if length(fpath), cd(fpath); end

if length(duration),
  my_delay = 100*duration/length(M);
end

axis tight;
j=1;
for itt = 1:length(M),
  P = frame2im(M(itt));
  imwrite(P,['/tmp/' fname '_' num2str(j) '.bmp'], 'bmp');
  j=j+1;
end

% make movie

disp(['Converting frames to '  fname '.gif']);

string = '! convert ';

if length(my_delay),
  string = [string ' -delay ' num2str(my_delay)]; 
end

for it = 1:j-1,  
  string = [string ' /tmp/' fname '_' num2str(it) '.bmp']; 
end
string = [string ' ' fname '.gif'];
eval(string);
