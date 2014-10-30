# Process all abundance and cost data for building the proteomap
#
# o collect all non-mapped genes in category "non-mapped"
# o omit all nan values
# o sum over all values for multiply occurring genes
#
# infile ".._abundance_.." -> outfile ".._abundance_NonMappedLumped_.."
# infile ".._cost_.."      -> outfile ".._cost_NonMappedLumped_.."
#                          -> outfile KO_hierarchy_standardised_SomeNonMapped.tms
#                          -> outfile <ORGANISM>_mapping_final_SomeNonMapped.csv

import sys
import os
import glob
import re
import numpy as np
import re
import math

from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy
from relevant_ko import relevant_ko


# which fraction of nonmapped proteins will be lumped to one polygon?
fraction_nonmapped_lumped = 0.005

# how many nonmapped proteins will be shown maximally?
n_nonmapped_displayed = 500


def prune_nonmapped_proteins_one_data_set(fi1,fo1,fo1l,fi_hierarchy,fo_hierarchy,fo_hierarchy_pos,nonmapped_dict,my_organism):
  
  # set of all gene names to be explicitly shown in the non-mapped region of some proteomap
  nonmapped_show = set()
  nonmapped_show_KO = set()
  
  sum_mapped    = 0
  sum_nonmapped = 0
  value_dict    = {}

  igot          = fi1.readlines()
  for line in igot:
    tt      = re.split("\t",line.strip())
    my_gene = tt[0]
    my_gene_names = re.split(';',my_gene)
    my_gene  = my_gene_names[0]
    my_value = float(tt[1])
    if not(math.isnan(my_value)):
      if my_gene in nonmapped_dict:
        sum_nonmapped = sum_nonmapped + my_value
      else:
        sum_mapped = sum_mapped + my_value
      if my_gene in value_dict:
        value_dict[my_gene] = value_dict[my_gene] + my_value
      else:
        value_dict[my_gene] = my_value
    sum_all = sum_mapped + sum_nonmapped

  print " Removing values below " + str(sum_all/(2500*2500))  + " (1 pixel)"
  print " Fraction of nonmapped: " + str(sum_nonmapped/sum_all)
  print " Total: " + str(sum_all)
  print " Total nonmapped: " + str(sum_nonmapped)

  # -------------------------------------------------------- 
  # compute threshold value s.t. sum of lumped protein mass
  # abundances is less than 0.5% (of non-mapped area)

  v = sorted([value_dict.get(gene,0) for gene in nonmapped_dict])
  v = np.array(v)
  v /= v.sum()

  # criterion 1: fixed percentage of non-mapped area to be lumped
  i_area_percentage = np.sum(np.cumsum(v) < fraction_nonmapped_lumped)

  # criterion 2:fixed maximal number of non-mapped proteins to be shown
  n_nonzero = 0
  for aa in v:
    if aa>0.:
      n_nonzero = n_nonzero + 1

  nn = min(n_nonmapped_displayed,n_nonzero)
  i = max(len(v) - nn,0)
  i = min(i,i_area_percentage)
  threshold = v[i]

  # -------------------------------------------------------- 

  sum_nonmapped_lumped = 0

  for my_gene in value_dict:
    if my_gene in nonmapped_dict:
      # keep only values that are above threshold
      if value_dict[my_gene] >= threshold * sum_nonmapped:
        nonmapped_show.add(my_gene)
        value_string = '%(value).8g' % {'value': value_dict[my_gene]}
        fo1.write(my_gene + "\t" + value_string + "\n")
      else:
        sum_nonmapped_lumped = sum_nonmapped_lumped + value_dict[my_gene]
        fo1l.write(my_gene + "\t" + str(value_dict[my_gene]) + "\n")
    else:
      # keep only values that yield an area of one pixel at least
      if value_dict[my_gene] > sum_all/(2500*2500):
        value_string = '%(value).8g' % {'value': value_dict[my_gene]}
        fo1.write(my_gene + "\t" + value_string + "\n")
      else:
        sum_nonmapped_lumped = sum_nonmapped_lumped + value_dict[my_gene]
        fo1l.write(my_gene + "\t" + str(value_dict[my_gene]) + "\n")
  sum_nonmapped_lumped_string = '%(value).8g' % {'value': sum_nonmapped_lumped}
  fo1.write("OtherNotMapped\t" + sum_nonmapped_lumped_string + "\n")

  print " Number of nonmapped proteins shown: " + str(len(nonmapped_show))
  print " Lumped within nonmapped: " + str(sum_nonmapped_lumped)
  print " Fraction of lumped within nonmapped: " + str(sum_nonmapped_lumped/sum_nonmapped)

  for my_gene in nonmapped_dict:
    if my_gene in nonmapped_show:
      nonmapped_show_KO.add(my_organism + "_" + my_gene)

  #--------------------------------------------------------------------
  # Write hierarchy file with (some) non-mapped proteins

  # copy old file
  igot = fi_hierarchy.readlines()
  for line in igot:
    fo_hierarchy_pos.write(line)
    # remove position brackets
    line = re.sub("\(.*,.*\)","",line)
    fo_hierarchy.write(line)  
  
  # add nonmapped genes
  for my_gene in nonmapped_dict:
    if my_gene in nonmapped_show:
      fo_hierarchy.write("\t\t\t\t" + my_organism + "_" + my_gene + "\n")
      fo_hierarchy_pos.write("\t\t\t\t" + my_organism + "_" + my_gene + "\n")

  #--------------------------------------------------------------------
  # Write mapping files "final.." and "..final_lumped.."

  #my_added_ko = rk.get_added_ko_dictionary()
  #
  #systematic_to_ko_gene = hh.get_mapping_systematic_to_ko_gene(my_organism,my_added_ko)
  #
  ## only mapped genes
  #for my_systematic in systematic_to_ko_gene:
  #  my_ko   = systematic_to_ko_gene[my_systematic]["ko"]
  #  my_gene = systematic_to_ko_gene[my_systematic]["gene"]
  #  if not (my_systematic in nonmapped_dict):
  #    fo_mapping.write(my_ko + "\t" + my_gene + ":" + my_systematic + "\n")
  #    fol_mapping.write(my_ko + "\t" + my_gene + ":" + my_systematic + "\n")
  #fo_mapping.close()

  # additionally, nonmapped genes
  #fol_mapping.write("NotMapped\tOther unmapped:OtherNotMapped\n")  
  #for my_gene in nonmapped_dict:
  #  if my_gene in nonmapped_show:
  #    fol_mapping.write(my_organism + "_" + my_gene + "\t" + my_gene + ":" + my_gene + "\n")
  #fol_mapping.close()

  return nonmapped_show, nonmapped_show_KO

# end of function

# -------------------------------------------------------------
# main program

def prune_nonmapped_proteins(data_dir):
  
  pp = proteomaps_path_names(data_dir)
  hh = proteomaps_hierarchy(data_dir)
  rk = relevant_ko(data_dir)
  
  data_files    = pp.get_data_files()
  organism_list = pp.get_organism_list()
  
  nonmapped_show_KO = set()
  nonmapped_show    = {}
  all_nonmapped_dict= {}
  
  for my_organism in pp.organism_list:
    nonmapped_show[my_organism] = set()
    all_nonmapped_dict[my_organism] = set()
  
  for my_file in data_files:
  
    filenames   = pp.get_filenames(my_file)
    my_organism = filenames['organism']
    mapping_filenames = pp.get_mapping_files(my_organism)
    print "\n" + my_organism + ' // ' + filenames['data_set']
  
    # for each organism: load list of nonmapped proteins 
    print filenames['nonmapped']
    fmappings = open(filenames['nonmapped'],"r")
    igot = fmappings.readlines()
    for line in igot:
      tt = re.split("\t",line.strip())
      #if tt[2] == 'NotMapped':
      q = re.split(":",tt[1])
      my_gene       = q[0]
      all_nonmapped_dict[my_organism].add(my_gene)
      #  #my_gene_names = re.split(';',my_gene)
      #  #my_gene       = my_gene_names[0]
      #  all_nonmapped_dict[my_organism].add(my_gene)
  
    print len(all_nonmapped_dict[my_organism])
  
    # -------------------------------------------------------------
    # process data file with length-weighted abundances
  
    print " WEIGHTED ABUNDANCE"
    fi1          = open(filenames['cost'],"r")
    fo1          = open(filenames['cost_lumped'],"w")
    fo1l         = open(filenames['cost_lumped_proteins'],"w")
    fi_hierarchy = open(pp.OUTFILE_KO_HIERARCHY_FILE_2 ,'r')
    fo_hierarchy = open(filenames['hierarchy_cost_lumped'],"w")
    fo_hierarchy_pos = open(filenames['hierarchy_cost_lumped_pos'],"w")
    #fo_mapping   = open(mapping_filenames['final'],"w")
    #fol_mapping  = open(filenames['mapping_cost_lumped'],"w")
  
    [my_nonmapped_show, my_nonmapped_show_KO] = prune_nonmapped_proteins_one_data_set(fi1,fo1,fo1l,fi_hierarchy,fo_hierarchy,fo_hierarchy_pos,all_nonmapped_dict[my_organism],my_organism)
    nonmapped_show[my_organism] = nonmapped_show[my_organism].union(my_nonmapped_show)
    nonmapped_show_KO = nonmapped_show_KO.union(my_nonmapped_show_KO)
    
    # -------------------------------------------------------------
    # process data file with (non-weighted) abundances
  
    print " ABUNDANCE"
    fi1          = open(filenames['abundance'],"r")
    fo1          = open(filenames['abundance_lumped'],"w")
    fo1l         = open(filenames['abundance_lumped_proteins'],"w")
    fi_hierarchy = open(pp.OUTFILE_KO_HIERARCHY_FILE_2 ,'r')
    fo_hierarchy = open(filenames['hierarchy_abundance_lumped'],"w")
    fo_hierarchy_pos = open(filenames['hierarchy_abundance_lumped_pos'],"w")
    #fo_mapping   = open(mapping_filenames['final'],"w")
    #fol_mapping  = open(filenames['mapping_abundance_lumped'],"w")
  
    [my_nonmapped_show, my_nonmapped_show_KO]  = prune_nonmapped_proteins_one_data_set(fi1,fo1,fo1l,fi_hierarchy,fo_hierarchy,fo_hierarchy_pos,all_nonmapped_dict[my_organism],my_organism)
    nonmapped_show[my_organism] = nonmapped_show[my_organism].union(my_nonmapped_show)
    nonmapped_show_KO = nonmapped_show_KO.union(my_nonmapped_show_KO)
  
  
  # ----------------------------------------
  # copy hierarchy file to hierarchy file with non-mapped genes for all datasets
  
  fi_hierarchy     = open(pp.OUTFILE_KO_HIERARCHY_FILE_2 ,'r')
  fo_hierarchy_all = open(pp.OUTFILE_KO_HIERARCHY_FILE_3 ,'w')
  
  igot = fi_hierarchy.readlines()
  for line in igot:
    fo_hierarchy_all.write(line)  
  
  for line in sorted(nonmapped_show_KO):
    fo_hierarchy_all.write("\t\t\t\t" + line + "\n")
  
  
  # ----------------------------------------
  # Write mapping files "final.." and "..final_lumped.."
  
  for my_organism in pp.organism_list:
    mapping_filenames = pp.get_mapping_files(my_organism)
    fo_mapping   = open(mapping_filenames['final'],"w")
    fol_mapping  = open(mapping_filenames['final_some_unmapped'],"w")
  
    my_added_ko           = rk.get_added_ko_dictionary()  
    systematic_to_ko_gene = hh.get_mapping_systematic_to_ko_gene(my_organism,my_added_ko)
    
    # only mapped genes
    for my_systematic in systematic_to_ko_gene:
      my_ko   = systematic_to_ko_gene[my_systematic]["ko"]
      my_gene = systematic_to_ko_gene[my_systematic]["gene"]
      if not (my_systematic in all_nonmapped_dict[my_organism]):
        fo_mapping.write(my_ko + "\t" + my_gene + ":" + my_systematic + "\n")
        fol_mapping.write(my_ko + "\t" + my_gene + ":" + my_systematic + "\n")
    fo_mapping.close()
  
    # additionally, nonmapped genes
    fol_mapping.write("NotMapped\tOther unmapped:OtherNotMapped\n")  
    for my_gene in all_nonmapped_dict[my_organism]:
      if my_gene in nonmapped_show[my_organism]:
        fol_mapping.write(my_organism + "_" + my_gene + "\t" + my_gene + ":" + my_gene + "\n")
    fol_mapping.close()

if __name__ == "__main__":
  prune_nonmapped_proteins(sys.argv[1])
