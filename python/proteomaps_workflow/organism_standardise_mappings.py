# write mapping files

import os
import glob
import re
import sys
from proteomaps_path_names import proteomaps_path_names
from proteomaps_hierarchy  import proteomaps_hierarchy
from proteomaps_hierarchy  import relevant_ko

data_dir = sys.argv[1]

pp = proteomaps_path_names(data_dir)
hh = proteomaps_hierarchy(data_dir)
rk = relevant_ko(data_dir)

organism_list = pp.get_organism_list()
relevant_ko   = rk.read_relevant_ko(pp.FILE_RELEVANT_KO)

# -------------------------------------------------
# make dictionaries relating gene names, KO numbers, etc

[ko_to_genes, ko_to_orfs, genes_to_ko, systematic_to_ko, ko_to_genes_completed, ko_to_orfs_completed] = hh.get_ko_mappings(organism_list,relevant_ko)


# -------------------------------------------------
# save standardised gene mappings

for organism_name in organism_list:

  mapping_filenames = pp.get_mapping_files(organism_name)

  f  = open(mapping_filenames['standardised'], 'w')
  f1 = open(mapping_filenames['standardised_genepair'], 'w')
  f2 = open(mapping_filenames['standardised_pair'], 'w')

  for my_ko in ko_to_genes_completed[organism_name]:

    my_genes = ko_to_genes_completed[organism_name][my_ko]
    my_orfs  = ko_to_orfs_completed[organism_name][my_ko]
    f.write(my_ko + "\t" + my_genes  + "\n")

    my_genes_list = re.split(' ', my_genes)
    for my_gene in my_genes_list:
      f1.write( my_ko + "\t" + my_gene + "\n")

    my_orfs_list = re.split(' ', my_orfs)
    for my_orf in my_orfs_list:
      f2.write( my_ko + "\t" + my_orf + "\n")

  f.write(  "NotMapped\tNotMapped\n")
  f1.write( "NotMapped\tNotMapped\n")
  f2.write( "NotMapped\tNotMapped\n")

  f.close()
