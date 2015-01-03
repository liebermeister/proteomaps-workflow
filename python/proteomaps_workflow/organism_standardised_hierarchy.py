import os
import glob
import re
import sys
from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy
from relevant_ko import relevant_ko

# -------------------------------------------------------------

def organism_standardised_hierarchy(data_dir,pp):
  
  #pp = proteomaps_path_names(data_dir)
  hh = proteomaps_hierarchy(data_dir,pp)
  rk = relevant_ko(data_dir,pp)
  
  organism_list  = pp.get_organism_list()
  my_relevant_ko = rk.all_relevant_ko()
  ko_to_genes    = hh.get_ko_mapping_one(organism_list,my_relevant_ko)
  
  # -------------------------------------------------------------
  
  for organism_name in organism_list:
  
    # go through hierarchy and collect all lines that are category names
    outfile = data_dir + "/hierarchy/" + organism_name + "_hierarchy_standardised.tms"
    fi = open(pp.OUTFILE_KO_HIERARCHY_FILE_1, 'r')
    fo = open(outfile, 'w')
    fo.write(organism_name+"\n")
    iigot = fi.readlines()
    my_level = []
    for lline in iigot:
      if lline[0:3] == "\t\t\t":
        my_level.append(3)
      elif lline[0:2] == "\t\t":
        my_level.append(2)
      elif lline[0:1] == "\t":
        my_level.append(1)
      else: 
        my_level.append(0)
    my_level.append(0)
    my_level.append(0)
  
    # go through hierarchy again, write out completed hierarchy
    z = 0
    for lline in iigot:
      if lline[0:3] == "\t\t\t":
        my_ko = lline[3:].strip()
        if my_ko in ko_to_genes[organism_name]:
          fo.write("\t\t\t\t" + my_ko + "\n")
      else:
        if my_level[z+1] > my_level[z]:
          if my_level[z] == 1 and my_level[z+2] ==3:
            fo.write("\t" + lline)
          if my_level[z] == 2 and my_level[z+1] ==3:
            fo.write("\t" + lline)
          if my_level[z] == 0 and my_level[z+3] ==3:
            fo.write("\t" + lline)
      z = z + 1
    fo.close()

if __name__ == "__main__":
  organism_standardised_hierarchy(sys.argv[1])
