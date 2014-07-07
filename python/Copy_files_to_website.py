# -----------------------------------------------------------------------------------------------
# Script for copying files to proteomaps website directory
# -----------------------------------------------------------------------------------------------

import subprocess
import sys
import os
import csv
import glob
import shutil
import re

# ==========================================================

def copy_files(data_set_collections):

  data_set_names = []
  data_set_to_collection = {}
  
  for data_set_collection in data_set_collections:
      filenames_file = '/home/wolfram/Proteomaps/data_sets/protein_abundances_' + data_set_collection + '/filenames.csv'
      for row in csv.reader(open(filenames_file, 'r'), delimiter='\t'):
  	organism, data_file_path, data_set_name, data_set_name_matlab, article_name = row
  	data_set_names.append(data_set_name)
  	data_set_to_collection[data_set_name] = data_set_collection
  
  # -----------------------------------------------------------------------------------------------
  # Copy the html files from intermediate directory proteomaps/html to website directory
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      for f in glob.glob('/home/wolfram/Proteomaps/data_html/' + data_set_name + '_*.html'):
          dum = re.split("/",f) 
          shutil.copyfile(f, '/home/wolfram/Proteomaps/proteomaps_online/data_sets/' + data_set_name + '/' + dum[-1])
  
  # -----------------------------------------------------------------------------------------------
  # copy jpg and png files to website directories
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      print data_set_name
      proteomaps_directory = data_set_to_collection[data_set_name]
      for f in glob.glob('/home/wolfram/Proteomaps/data_sets/paver_output_data/proteomaps_' + proteomaps_directory + '/jpg/' + data_set_name + '*.jpg'):
          dum = re.split("/",f) 
          shutil.copyfile(f, '/home/wolfram/Proteomaps/proteomaps_online/data_sets/' + data_set_name + '/pictures/' + dum[-1])
      for f in glob.glob('/home/wolfram/Proteomaps/data_sets/paver_output_data/proteomaps_' + proteomaps_directory + '/png/' + data_set_name + '*.png'):
          dum = re.split("/",f) 
          shutil.copyfile(f, '/home/wolfram/Proteomaps/proteomaps_online/data_sets/' + data_set_name + '/pictures/' + dum[-1])

  # -----------------------------------------------------------------------------------------------
  # Copy csv data files to website directories
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      proteomaps_directory = data_set_to_collection[data_set_name]
      subprocess.call(['cp','/home/wolfram/Proteomaps/data_sets/protein_abundances_' + proteomaps_directory + "/" + data_set_name + '/' + data_set_name + '.csv', '/home/wolfram/Proteomaps/proteomaps_online/data_sets/' + data_set_name + "/"])


# ==========================================================
# Main program

# Which data set collections should be copied to the website?
# (You need to create the html files before by running make_proteomaps_html.py)

data_set_collections = {'paper'} #  'other', 'geiger_cell_lines', 'valgepea_ecoli', 'khan_human_chimp', 'krizhanovsky', 'geiger_mouse',}

copy_files(data_set_collections)
