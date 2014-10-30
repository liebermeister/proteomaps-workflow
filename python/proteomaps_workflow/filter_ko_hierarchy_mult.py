# Same as filter_ko_hierarchie.py, BUT:
# multiply occurring KO numbers are kept except for KEGG numbers that are
# explicitly assigned to one category by the file KO_gene_hierarchy_changes.csv
# output: [TMP_DIR]/KO_hierarchy_standardised_multiple_occurance_[NUMBER].tms
#
# 1. read KO hierarchy
# 2. filter it for KO numbers appearing the list KO_relevant.csv
#    (representing KO numbers appearing in the protein data)
# 3. add all entries requested in file ../proteomaps/KO_gene_hierarchy/KO_gene_hierarchy_organism_mapping/KO_gene_hierarchy_changes.csv
# 4. Write our new hierachy

import os
import glob
import re
import sys
import random
import copy

from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy
from relevant_ko import relevant_ko

# ----------------------------------------------

def filter_ko_hierarchy_mult(data_dir,n_resample):

  pp = proteomaps_path_names(data_dir)
  hh = proteomaps_hierarchy(data_dir)
  rk = relevant_ko(data_dir)
  
  organism_list = set(pp.get_organism_list())
  
  my_relevant_ko        = rk.read_relevant_ko(pp.FILE_RELEVANT_KO)
  pathways_in_hierarchy = hh.get_pathways_in_original_hierarchy()
  
  # -----------------------------------------------------------
  ## read file KO_gene_hierarchy_changes.csv containing genes to be added to the hierarchy
  # (overriding possibly existing entries)
  
  [my_added_ko, all_added_ko] = rk.get_added_ko_2(pathways_in_hierarchy)
  
  fi = open(pp.INFILE_KO_HIERARCHY_FILE, 'r')
  
  
  igot = fi.readlines()
  
  ko_fixed_by_input_table = [];
  ko_counter = {};
  outlines = []
  levels   = []
  for line in igot:
      if line[0:3] == "\t\t\t":
          my_ko = line[3:].strip()
          if my_ko in my_relevant_ko:
              if not my_ko in all_added_ko:
                  if not my_ko in ko_fixed_by_input_table:
                      if my_ko in ko_counter:
                          ko_counter[my_ko] = ko_counter[my_ko]+1
                      else:
                          ko_counter[my_ko] = 1                        
                      outlines.append("\t\t\t" + my_ko + "\n")
                      levels.append(3)
      elif line[0:2] == "\t\t":
          outlines.append(line)
          levels.append(2)
          my_pathway = line.strip()
          if my_pathway in my_added_ko:
              for my_ko in my_added_ko[my_pathway]:
                  if not my_ko in ko_fixed_by_input_table:
                      outlines.append("\t\t\t" + my_ko + "\n")
                      ko_fixed_by_input_table.append(my_ko)
                      ko_counter[my_ko] = 1
                      levels.append(3)
      elif line[0:1] == "\t":
          outlines.append(line)
          levels.append(1)
      else:
          outlines.append(line)
          levels.append(0)
  
  levels.append(0)
  levels.append(0)
  levels.append(0)
  
  for it in range(int(n_resample)):
  
      print "Randomised assignment " + str(it+1) + "/" + str(n_resample) 
      
      # ------------------------------------------------------
      ## go through the hierarchy again; for each ko number, count how often it
      ## already appeared: then, compute with what probability it should be accepted
      ## this time. example: it appears 3 times in total (known from ko_counter[my_ko])
      ## on its first appearance, the acceptance probability is 1/3; if it's not accepted
      ## this time, then next time it's 1/2; and next time, 1.
  
      this_ko_counter = ko_counter.copy()
      this_ko_counter_seen = {}
      this_outlines = []
      this_levels   = []
      z = 0
  
      for line in outlines:
          if (levels[z] == 3):
              my_ko = line.strip()
              if my_ko in this_ko_counter_seen:
                  this_ko_counter_seen[my_ko] = this_ko_counter_seen[my_ko] + 1
              else:
                  this_ko_counter_seen[my_ko] = 1
              # print my_ko + "\t" + str(this_ko_counter_seen[my_ko]) + "\t" + str(this_ko_counter[my_ko])
              if this_ko_counter[my_ko]>0:
                  prob = 1/ float(this_ko_counter[my_ko] - (this_ko_counter_seen[my_ko] - 1))
                  my_rand = random.random()
                  if my_rand < prob:
                      this_outlines.append(line)
                      this_levels.append(levels[z])
                      this_ko_counter[my_ko] = 0
          else:
              this_outlines.append(line)
              this_levels.append(levels[z])
          z = z + 1
      this_levels.append(0)
      this_levels.append(0)
      this_levels.append(0)
  
      # ------------------------------------------------------
      ## write out result
  
      fo = open(pp.TMP_DIR + "/KO_hierarchy_standardised_multiple_occurance" + "_" + str(it+1) + ".tms", 'w')
  
      z = 0
      for line in this_outlines:
          fo.write(line)
          z = z + 1
  
      fo.write("Not Mapped\n")
      fo.write("\tNot Mapped\n")
      fo.write("\t\tNot mapped\n")
      fo.write("\t\t\tNotMapped\n")
  
      fo.close()

if __name__ == "__main__":
  filter_ko_hierarchy_mult(sys.argv[1],sys.argv[2])
