import re
import sys
import subprocess
from proteomaps_path_names import proteomaps_path_names

# ---------------------------------------------------------
# TO DO:
#  implement maps with abundance instead of cost
#  use hierarchy files without unnecessary branches and without polytope positions

data_dir = sys.argv[1]

pp = proteomaps_path_names(data_dir)

PYTHON_PATH = '/home/wolfram/projekte/protein_abundance/python/avi_d3_treemaps/treemaps-master/scripts/'
TREEMAP_DIR = '/home/wolfram/projekte/protein_abundance/html/d3_treemaps/ui/'

color_file = pp.OUTFILE_KO_COLOR_FILE

print 'Writing files to directory ' + TREEMAP_DIR

for data_file_triple in pp.data_files:
  filenames = pp.get_filenames(data_file_triple)
  data_set      = filenames['data_set']
  hierachy_file = filenames['hierarchy_cost_lumped']
  data_file     = filenames['cost_lumped']
  organism_name = filenames['organism']

  mapping_filenames = pp.get_mapping_files(organism_name)
  mapping_file = mapping_filenames['final_some_unmapped']
  
  # ----------------------------------------------------------

  json_file1          = TREEMAP_DIR + '/data/hierarchy_' + data_set + '.json'
  json_file2          = data_set + '.json'
  index_file_template = TREEMAP_DIR + 'index_TEMPLATE.html'
  index_file          = TREEMAP_DIR + data_set + '.html'
  
  # ----------------------------------------------------------------------
  # call avi's code for creating the json files
  
  p = subprocess.Popen(['python', PYTHON_PATH + 'make_json_hierarchy.py', '-c', color_file, hierachy_file, json_file1])
  p.wait()
  
  p = subprocess.Popen(['python', PYTHON_PATH + 'apply_values.py', json_file1, data_file, mapping_file, TREEMAP_DIR + json_file2])
  p.wait()
  
  # ----------------------------------------------------------------------
  # copy index file and replace filename
  
  fi = open(index_file_template,'r')
  fo = open(index_file,'w')
  
  igot = fi.readlines()
  
  for line in igot:
    line = re.sub('FILENAME',json_file2,line)
    fo.write(line)
