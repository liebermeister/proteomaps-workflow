import sys
import os
import glob
import re
import math

from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy import proteomaps_hierarchy

# ----------------------------------------------

def make_csv_tables(data_dir):

  pp = proteomaps_path_names(data_dir)
  hh = proteomaps_hierarchy(data_dir)
  
  data_files    = pp.get_data_files()
  organism_list = pp.get_organism_list()
  
  
  # -----------------------------------------------------------------------
  # import the mappings from systematic names to gene names
  # import the mappings from systematic names to KO numbers from regular kegg files
  
  systematic_to_gene = {}
  systematic_to_ko   = {}
  
  for organism_name in organism_list:
      systematic_to_gene[organism_name] = {}
      systematic_to_ko[organism_name] = {}
      mapping_filenames = pp.get_mapping_files(organism_name)
      f = open(mapping_filenames['final'], 'r')
      igot = f.readlines()
      for line in igot:
          q          = re.split('\t', line.strip())
          if len(q)>1:
            r          = re.split(':', q[1])
            if len(r) > 1:
              ko         = q[0]
              gene       = r[0]
              systematic = r[1]
              systematic_to_gene[organism_name][systematic] = gene
              systematic_to_ko[organism_name][systematic]   = ko
      f.close()
  
  
  # -----------------------------------------------------------------------
  # import mapping from ko numbers to ko categories
  # yields dictionary ko numbers -> ko categories
  
  ko_to_category = hh.get_ko_to_category(organism_list)
  
  
  # -------------------------------------------------------------
  # load processed data
  
  for data_file_triple in data_files:
      my_organism = data_file_triple[1]
      filenames   = pp.get_filenames(data_file_triple)
      print 'Processing file ' + my_organism + ' // ' + filenames['short']
  
      fi_abundance = open(filenames['abundance'],"r")
      fi_cost      = open(filenames['cost'],"r")
  
      # ---------------------------------------------------------
      # Read abundance values 
  
      systematic_to_abundance_ppm = {}
      systematic_to_abundance     = {}
  
      # compute the sum first
      igot = fi_abundance.readlines()
      fi_abundance.close()
  
      sum_value = 0    
      for line in igot:
         q = re.split('\t', line.strip())
         my_value = float(q[1])
         if not(math.isnan(my_value)):
           sum_value = sum_value + my_value
  
      all_systematic     = []
  
      for line in igot:
         q = re.split('\t', line.strip())
         systematic  = q[0]
         if not(systematic in all_systematic):
           all_systematic.append(systematic)
         value = float(q[1])
         ppm   = str(1000000 * value / sum_value)
         value = '%s' % float('%.10g' % value)
         if systematic in systematic_to_abundance_ppm:
           systematic_to_abundance_ppm[systematic].append(ppm)
           systematic_to_abundance[systematic].append(value)
         else:
           systematic_to_abundance_ppm[systematic] = [ppm] 
           systematic_to_abundance[systematic] = [value]
  
      # ---------------------------------------------------------
      # Read cost values 
  
      systematic_to_cost_ppm = {}
      systematic_to_cost     = {}
  
      # compute the sum first
      igot = fi_cost.readlines()
      fi_abundance.close()
  
      sum_value = 0    
      for line in igot:
         q = re.split('\t', line.strip())
         my_value  = float(q[1])
         if not(math.isnan(my_value)):
           sum_value = sum_value + my_value
  
      for line in igot:
         q = re.split('\t', line.strip())
         systematic  = q[0]
         value = float(q[1])
         ppm   = str(1000000 * value / sum_value)
         value = '%s' % float('%.8g' % value)
         if systematic in systematic_to_cost_ppm:
           systematic_to_cost_ppm[systematic].append(ppm)
           systematic_to_cost[systematic].append(value)
         else:
           systematic_to_cost_ppm[systematic] = [ppm] 
           systematic_to_cost[systematic] = [value]
  
      fi_abundance.close()
  
      # ---------------------------------------------------------
      # Read length values 
  
      systematic_to_length = hh.get_protein_lengths(my_organism,350)
  
      # ----------------------------------------------------------------------
      # write table to output file
  
      my_data_set = data_file_triple[2]
      outfile = data_dir + "/" + my_data_set + "/" + my_data_set + ".csv"
      print "Writing file " + outfile
      fo_abundance = open(outfile,"w")
      fo_abundance.write("!!SBtab TableType='Proteomaps'")
      fo_abundance.write(" Organism='" + my_organism + "'")
      if my_organism == 'hsa':
          fo_abundance.write(" ProteinIdentifier='http://identifiers.org/uniprot/'\n")
      elif my_organism == 'sce':
          fo_abundance.write(" ProteinIdentifier='http://http://identifiers.org/sgd/'\n")
      fo_abundance.write("!ProteinIdentifier\t!Abundance[original])\t!Abundance[ppm]\t!SizeWeightedAbundance[original]\t!SizeWeightedAbundance[ppm]\t!ProteinSize\t!ProteinName\t!Identifiers:kegg.orthology\t!Pathway\n")
  
      for systematic in all_systematic:
        
        if systematic in systematic_to_length:
          length = systematic_to_length[systematic]
        else:
          length = '350'
  
        # extra information (right columns)
        wline_end = str(length)
        
        if systematic in systematic_to_gene[my_organism].keys():
          my_gene = systematic_to_gene[my_organism][systematic]
          my_ko   = systematic_to_ko[my_organism][systematic]
          if my_ko in ko_to_category:
            my_category = ko_to_category[my_ko]
          else:
            my_category = ''
          if not my_ko[0] == 'K':
            my_ko = ''
          if my_category == 'Not mapped':
            my_category = ''
          wline_end = wline_end + "\t" + my_gene + "\t" + my_ko + "\t" + my_category
        else:
          wline_end = wline_end + "\t\t\t"
  
        for it in range(0,len(systematic_to_abundance[systematic])):
          abundance      = systematic_to_abundance[systematic][it]
          abundance_ppm  = systematic_to_abundance_ppm[systematic][it]
          cost           = systematic_to_cost[systematic][it]
          cost_ppm       = systematic_to_cost_ppm[systematic][it]
  
          wline = systematic + "\t" + abundance + "\t" + abundance_ppm + "\t" + cost + "\t" + cost_ppm  + "\t" + wline_end
          fo_abundance.write(wline + "\n")
  
      fo_abundance.close()

if __name__ == "__main__":
  make_csv_tables(sys.argv[1])
