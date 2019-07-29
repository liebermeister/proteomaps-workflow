# prepare input files for paver:
# copy some of the workflow's result files to a special directory
# and tgz it (currently commented out)

import sys
import os
import subprocess
import re
import csv
import argparse
from proteomaps_path_names import proteomaps_path_names

# ---------------------------------------------------------------
# command line arguments

parser = argparse.ArgumentParser(description='Proteomaps data processing workflow')
parser.add_argument('data_set_directory',   help='directory name for data set bundle')
parser.add_argument('paver_input_file_directory', help='directory name for paver input files')
parser.add_argument('hierarchy_version', help='subdirectory with hierarchy data')
args = parser.parse_args()

print(args.data_set_directory)
print(args.paver_input_file_directory)
 
# ---------------------------------------------------------------
# read data file names

verbose = 1

pp = proteomaps_path_names(args.data_set_directory,args.hierarchy_version,verbose)
data_file_triples = pp.get_data_files()

data_files = []

for data_file_triple in data_file_triples:
  filenames = pp.get_filenames(data_file_triple)
  data_files.append({})
  data_files[-1]['in']  = filenames['cost_lumped']
  data_files[-1]['out'] = filenames['data_set'] + "_cost.csv"
  # data_files.append({})
  # data_files[-1]['in']  = filenames['mapping_cost_lumped']
  # data_files[-1]['out'] = filenames['data_set'] + "_cost_mapping.csv"
  data_files.append({})
  data_files[-1]['in']  = filenames['hierarchy_cost_lumped_pos']
  data_files[-1]['out'] = filenames['data_set'] + "_cost_hierarchy.tms"
  data_files.append({})
  data_files[-1]['in']  = filenames['abundance_lumped']
  data_files[-1]['out'] = filenames['data_set'] + "_abundance.csv"
  # data_files[-1]['in']  = filenames['mapping_abundance_lumped']
  # data_files[-1]['out'] = filenames['data_set'] + "_abundance_mapping.csv"
  data_files.append({})
  data_files[-1]['in']  = filenames['hierarchy_abundance_lumped_pos']
  data_files[-1]['out'] = filenames['data_set'] + "_abundance_hierarchy.tms"
  data_files.append({})
  data_files[-1]['in']  = filenames['processed_data']
  data_files[-1]['out'] = filenames['data_set'] + ".csv"

# ---------------------------------------------------------------
# copy files

subprocess.call(['mkdir', args.paver_input_file_directory])
subprocess.call(['rm','-r', args.paver_input_file_directory + '/data/'])
subprocess.call(['mkdir', args.paver_input_file_directory + '/data'])
#subprocess.call(['rm','-r', args.paver_input_file_directory + '/data/*'])

#subprocess.call(['cp', pp.OUTFILE_KO_HIERARCHY_FILE_3, 
#                       args.paver_input_file_directory + '/data/KO_hierarchy_some_unmapped.tms'])

subprocess.call(['cp', args.data_set_directory + '/hierarchy/KO_color_table.csv', 
                       args.paver_input_file_directory + '/data/KO_color_table.csv'])

for my_organism in pp.organism_list:
  mapping_filenames = pp.get_mapping_files(my_organism)
  print "- " + mapping_filenames['final_some_unmapped']
  subprocess.call(['cp', mapping_filenames['final_some_unmapped'], args.paver_input_file_directory  + '/data/KO_mapping_' + my_organism + '_some_unmapped.csv'])

for file in data_files:
  subprocess.call(['cp', file['in'], args.paver_input_file_directory  + "/data/" + file['out']])

# subprocess.call(['rm', '*tgz'])
# subprocess.call(['tar', '-cvzf', args.paver_input_file_directory + '/data.tgz', args.paver_input_file_directory + '/data'])

os.chdir(args.paver_input_file_directory)

subprocess.call(['clean_directories.pl'])
