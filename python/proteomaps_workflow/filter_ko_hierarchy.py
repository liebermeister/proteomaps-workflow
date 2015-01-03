# 1. read KO hierarchy from file ../gene_function_trees/KO_gene_hierarchy_organism_mapping/KO_hierarchy.csv
# 2. filter it for KO numbers appearing the list KO_relevant.csv
#    (representing KO numbers appearing in the protein data)
# 3. add all entries requested in file ../gene_function_trees/KO_gene_hierarchy_organism_mapping/KO_gene_hierarchy_changes.csv
# 4. Write our new hierachy

import os
import glob
import re
import csv
import sys

from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy
from relevant_ko import relevant_ko

# ----------------------------------------------

def filter_ko_hierarchy(data_dir,pp):

  #pp = proteomaps_path_names(data_dir)
  hh = proteomaps_hierarchy(data_dir,pp)
  rk = relevant_ko(data_dir,pp)

  INFILE_KO_HIERARCHY_FILE    = pp.INFILE_KO_HIERARCHY_FILE
  OUTFILE_KO_HIERARCHY_FILE_1 = pp.OUTFILE_KO_HIERARCHY_FILE_1
  OUTFILE_KO_HIERARCHY_FILE_2 = pp.OUTFILE_KO_HIERARCHY_FILE_2
  FILE_RELEVANT_KO            = pp.FILE_RELEVANT_KO
  
  pathways_in_hierarchy = hh.get_pathways_in_original_hierarchy()
  my_relevant_ko        = rk.read_relevant_ko(FILE_RELEVANT_KO)
  
  # read file KO_gene_hierarchy_changes.csv containing genes to be added to the hierarchy
  # (overriding possibly existing entries)

  [my_added_ko, all_added_ko] = rk.get_added_ko_2(pathways_in_hierarchy)

  filter_ko_hierarchy_from_files(INFILE_KO_HIERARCHY_FILE,OUTFILE_KO_HIERARCHY_FILE_1,OUTFILE_KO_HIERARCHY_FILE_2,my_relevant_ko,my_added_ko,all_added_ko)

def filter_ko_hierarchy_from_files(INFILE_KO_HIERARCHY_FILE,OUTFILE_KO_HIERARCHY_FILE_1,OUTFILE_KO_HIERARCHY_FILE_2,my_relevant_ko,my_added_ko,all_added_ko):
  # Argument my_relevant_ko can be empty list -> then all KO numbers are accepted 

  # -----------------------------------------------------------
  # go through hierarchy and write all lines that are
  #  - either no KO numbers
  #  - or KO numbers that appear in the relevant list
  # exclude all KO Numbers that already appeared before
  
  ko_appeared_already = []
  outlines            = []
  levels              = []

  # if list 'my_relevant_ko' is empty: accept any KO numbers:
  if len(my_relevant_ko)==0:
    my_relevant_ko = all_added_ko
    my_relevant_ko = []
    fi = open(INFILE_KO_HIERARCHY_FILE, 'r')
    igot = fi.readlines()
    for line in igot:
      my_relevant_ko.append(line.strip())

  fi = open(INFILE_KO_HIERARCHY_FILE, 'r')
  igot = fi.readlines()
  
  for line in igot:
      if line[0:3] == "\t\t\t":
          my_ko = line[3:].strip()
          if my_ko in my_relevant_ko:
              if not my_ko in all_added_ko:
                  if not my_ko in ko_appeared_already:
                      outlines.append("\t\t\t" + my_ko + "\n")
                      levels.append(3)
                      ko_appeared_already.append(my_ko)
      elif line[0:2] == "\t\t":
          outlines.append(line)
          levels.append(2)
          my_pathway = line.strip()
          if my_pathway in my_added_ko:
              for my_ko in my_added_ko[my_pathway]:
                  if not my_ko in ko_appeared_already:
                      outlines.append("\t\t\t" + my_ko + "\n")
                      levels.append(3)
                      ko_appeared_already.append(my_ko)
      elif line[0:1] == "\t":
          outlines.append(line)
          levels.append(1)
      else:
          outlines.append(line)
          levels.append(0)
  
  levels.append(0)
  levels.append(0)
  levels.append(0)
  
  # --------------------------------------------------------
  # write out result
  
  fo  = open(OUTFILE_KO_HIERARCHY_FILE_1, 'w')
  fop = open(OUTFILE_KO_HIERARCHY_FILE_2, 'w')
  
  is_ok    = len(outlines) * [0]
  ok_level = 0
  
  for z in reversed(range(0,len(outlines)-1)):
      if (levels[z] == 3):
          is_ok[z] = 1
          ok_level = 3
      elif levels[z] < ok_level:
          is_ok[z] = 1
          ok_level = levels[z]
  
  z = 0
  
  fop.write("KO\n")
  
  for line in outlines:
      do_print = is_ok[z]
      if do_print:
          fo.write(line)            
          if line.strip() == "Environmental Information Processing":
              line = "Environmental Information Processing (5,1)\n"
          if line.strip() == "Genetic Information Processing":
              line = "Genetic Information Processing (1,1)\n"
          if line.strip() == "Metabolism":
              line = "Metabolism (0,10)\n"
          if line.strip() == "Transcription":
              line = "\tTranscription (0,0)\n"
          if line.strip() == "Translation":
              line = "\tTranslation (0,4)\n"
          if line.strip() == "Biosynthesis":
              line = "\tBiosynthesis (0,6)\n"
          if line.strip() == "Energy Metabolism":
              line = "\tEnergy Metabolism (1,8)\n"
          if line.strip() == "Other Enzymes":
              line = "\tOther Enzymes (0,10)\n"
          if line.strip() == "Central Carbon Metabolism":
              line = "\tCentral Carbon Metabolism (4,8)\n"
          if line.strip() == "Membrane Transport":
              line = "\tMembrane Transport (5,9)\n"
          if line.strip() == "Cellular Processes":
              line = "Cellular Processes (6,9)\n"
          if line.strip() == "Organismal Systems":
              line = "Organismal Systems (7,9)\n"
          if line.strip() == "Human Diseases":
              line = "Human Diseases (8,9)\n"
          fop.write("\t" + line)
      z = z + 1
  
  fo.write("Not Mapped\n")
  fo.write("\tNot Mapped\n")
  fo.write("\t\tNot mapped\n")
  fo.write("\t\t\tNotMapped\n")
  
  fop.write("\tNot Mapped (10,0)\n")
  fop.write("\t\tNot Mapped\n")
  fop.write("\t\t\tNot mapped\n")
  fop.write("\t\t\t\tNotMapped\n")
  
  fo.close()

if __name__ == "__main__":
  filter_ko_hierarchy(sys.argv[1])
