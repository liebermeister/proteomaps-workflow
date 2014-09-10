# o make data directories if necessary
# o read original data file and write files for 
#   o abundance
#   o abundance (with ko numbers)
#   o abundance (with ko numbers and only for nonmapped genes)
#   o cost (size-weighted abundance)
#   o collected ko IDs

import sys
import os
import glob
import re

from math import log10, floor
from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy
from proteomaps_hierarchy import relevant_ko

# ----------------------------------------------

# Set default protein length of 350
standard_length = 350

data_dir = sys.argv[1]

pp = proteomaps_path_names(data_dir)
rk = relevant_ko(data_dir)
hh = proteomaps_hierarchy(data_dir)

systematic_to_gene = hh.systematic_to_gene
systematic_to_ko   = hh.systematic_to_ko
systematic_in_hierarchy = hh.systematic_in_hierarchy

data_files         = pp.get_data_files()

# -------------------------------------------------------------
# make directories (if they do not exist yet)

pp.make_data_file_directories()


# -------------------------------------------------------------
# for each data set:
# load original data and convert systematic name to gene name and KO number

for data_file_triple in data_files:
  filenames   = pp.get_filenames(data_file_triple)
  my_organism = filenames['organism']
  print my_organism + ' // ' + filenames['original_data']

  fi   = open(filenames['original_data'],"r")
  fo0  = open(filenames['abundance'],"w")
  fo1  = open(filenames['ko'],       "w")
  fo2  = open(filenames['nonmapped'],"w")

  name_list = []
  igot      = fi.readlines()
  for line in igot:
    if line[0]=="\t":
      print 'Warning (data set ' + filenames['data_set'] + ': Gene name missing'
    else:
      q    = re.split('\t', line.strip())
      name = q[0]
      chop_names = re.split(';',name)
      name = chop_names[0]
      if name in name_list:
        print 'Warning (data set ' + filenames['data_set'] + ': gene ' + name + ' has appeared before.'
      name_list.append(name)
      
      if len(q)>1:
        try:
          value = float(q[1])
          value_string = '%(value).8g' % {'value': value}
          fo0.write(name + "\t" + value_string + "\n")
          if name in systematic_to_gene[my_organism].keys():
            my_ko = systematic_to_ko[my_organism][name]
            fo1.write(name + "\t" + my_ko + "\t" + "\t" + value_string + "\n")
            if not(name in systematic_in_hierarchy[my_organism]):
              fo2.write(name + "\t" + name + "\t" + my_ko + "\t" + value_string + "\n")        
          else:
            fo1.write(name + "\tNotMapped\t" + "\t" + value_string + "\n")
            if not(name in systematic_in_hierarchy[my_organism]):
              fo2.write(name + "\t" + name + "\tNotMapped\t" + value_string + "\n")        
        except ValueError, TypeError:
          print "Non-numeric value " + q[1] + ". Line ignored."

  fo0.close()
  fo1.close()
  fo2.close()

  
# ---------------------------------------------
# collect ko ids in extra file

# read relevant ko ids
collected_ko = rk.all_relevant_ko()

# write relevant ko ids to file
rk.write_relevant_ko(collected_ko,pp.FILE_RELEVANT_KO)


# -------------------------------------------------------------
# make data files with cost (size-weighted abundance)

for data_file_triple in data_files:

  filenames   = pp.get_filenames(data_file_triple)
  my_organism = filenames['organism']

  print my_organism + ' // ' + filenames['data_set']
  
  protein_to_length = hh.get_protein_lengths(my_organism,standard_length)

  fi  = open(filenames['abundance'],"r")
  fo  = open(filenames['cost'],"w")

  igot = fi.readlines()
  for line in igot:
    tt    = re.split("\t",line.strip())
    prot  = tt[0]
    value = float(tt[1])
    if prot in protein_to_length:
      my_prot_length = protein_to_length[prot]
    else:
      my_prot_length = standard_length
    value_string = '%(value).8g' % {'value': my_prot_length * value}
    fo.write(prot + "\t" + value_string + "\n")
