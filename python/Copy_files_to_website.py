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

from proteomaps_PATHNAMES import proteomaps_PATHNAMES

# ==========================================================

def copy_files(data_set_collections, resize_pictures,hierarchy_version,BASE_DIR):

  data_set_names = []
  data_set_to_collection = {}
  
  for data_set_collection in data_set_collections:
      filenames_file = BASE_DIR + 'data_sets/protein_abundances_' + data_set_collection + '/filenames.csv'
      for row in csv.reader(open(filenames_file, 'r'), delimiter='\t'):
  	organism, data_file_path, data_set_name, data_set_name_matlab, article_name = row
  	data_set_names.append(data_set_name)
  	data_set_to_collection[data_set_name] = data_set_collection

  # -----------------------------------------------------------------------------------------------
  # Resize pictures
  # -----------------------------------------------------------------------------------------------

  if resize_pictures:
    for data_set_name in data_set_names:
      print data_set_name
      proteomaps_directory = data_set_to_collection[data_set_name]
      proteomaps_directory_full = BASE_DIR + 'data_paver_output/proteomaps_' + proteomaps_directory

      for f in glob.glob(proteomaps_directory_full + '/jpg/' + data_set_name + '*.jpg'):
        if not(re.search("_800.",f)):
          dum = re.split("/",f)
          print 'Resizing picture: writing file ' + f[:-4] + "_800.png"
          subprocess.call(['convert', '-quality','100', '-resize', '800x800', f, f[:-4] + "_800.png"])
          
      for f in glob.glob(proteomaps_directory_full + '/png/' + data_set_name + '*.png'):
        if not(re.search("_800.",f)):
          dum = re.split("/",f) 
          print 'Resizing picture: writing file ' + f[:-4] + "_800.png"
          subprocess.call(['convert', '-quality','100', '-resize', '800x800', f, f[:-4] + "_800.png"])
  
  # -----------------------------------------------------------------------------------------------
  # Copy the html files from intermediate directory proteomaps/html to website directory
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      for f in glob.glob(BASE_DIR + 'data_html/' + data_set_name + '_*.html'):
          dum = re.split("/",f)
          shutil.copyfile(f, BASE_DIR + 'proteomaps_online/data_sets/' + data_set_name + '/' + dum[-1])
      for f in glob.glob(BASE_DIR + 'data_html/' + data_set_name + '_*.js'):
          dum = re.split("/",f) 
          shutil.copyfile(f, BASE_DIR + 'proteomaps_online/data_sets/' + data_set_name + '/' + dum[-1])

  # -----------------------------------------------------------------------------------------------
  # copy jpg and png files to website directories
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      print data_set_name
      proteomaps_directory = data_set_to_collection[data_set_name]
      for f in glob.glob(BASE_DIR + 'data_paver_output/proteomaps_' + proteomaps_directory + '/jpg/' + data_set_name + '*.jpg'):
          dum = re.split("/",f) 
          shutil.copyfile(f, BASE_DIR + 'proteomaps_online/data_sets/' + data_set_name + '/pictures/' + dum[-1])
      for f in glob.glob(BASE_DIR + 'data_paver_output/proteomaps_' + proteomaps_directory + '/png/' + data_set_name + '*.png'):
          dum = re.split("/",f) 
          f_resized = f[:-4] + "_resized.png"
          shutil.copyfile(f, BASE_DIR + 'proteomaps_online/data_sets/' + data_set_name + '/pictures/' + dum[-1])
          
  # -----------------------------------------------------------------------------------------------
  # Copy csv data files to website directories
  # -----------------------------------------------------------------------------------------------
  
  for data_set_name in data_set_names:
      proteomaps_directory = data_set_to_collection[data_set_name]
      subprocess.call(['cp',BASE_DIR + 'data_sets/protein_abundances_' + proteomaps_directory + "/" + data_set_name + '/' + data_set_name + '.csv', BASE_DIR + 'proteomaps_online/data_sets/' + data_set_name + "/"])


# ==========================================================
# Main program

# Which data set collections should be copied to the website?
# (You need to create the html files before by running make_proteomaps_html.py)

data_set_collections = {'paper', 'geiger_cell_lines'} # {'other', 'new', 'valgepea_ecoli',  'geiger_mouse'}

# set resize_pictures to zero if the resizing has been done already
resize_pictures = 0

hierarchy_version = 'KO_gene_hierarchy_2014-08-01/'

BASE_DIR = "/home/wolfram/Proteomaps/"

copy_files(data_set_collections, resize_pictures,hierarchy_version,BASE_DIR)
