# ----------------------------------------------------
# Class functions for proteomaps hierarchy
# Filenames are taken from class proteomaps_path_names
# ----------------------------------------------------

import re
from proteomaps_path_names import proteomaps_path_names

class proteomaps_hierarchy:

  def __init__(self,data_dir):

    # gene name mapping information (combined information from organism mapping and annotation changes file)
    # stored in two dictionaries:
    #  systematic names -> gene names
    #  systematic names -> ko numbers
    # make them now:

    pp = proteomaps_path_names(data_dir)
    self.pp = pp

    # get all KO numbers in original hierarchy file
    fi = open(self.pp.INFILE_KO_HIERARCHY_FILE, 'r')
    igot = fi.readlines()
    KOs_in_original_hierarchy = set()
    for line in igot:
      if (line[0:3] == "\t\t\t"):
        KOs_in_original_hierarchy.add(line.strip())

    # Import mappings from systematic names to gene names and KO numbers from regular kegg files
    # -> dictionaries 'systematic_to_gene' and 'systematic_to_ko'

    systematic_to_gene = {}
    systematic_to_ko   = {}
    systematic_in_hierarchy = {}

    for organism_name in pp.get_organism_list():

      organism_mapping_file = pp.get_mapping_files(organism_name)
      systematic_to_gene[organism_name] = {}
      systematic_to_ko[organism_name] = {}
      systematic_in_hierarchy[organism_name] = set()
      f = open(organism_mapping_file['original'], 'r')
      igot = f.readlines()        
      for line in igot:
        q          = re.split('\t', line)
        systematic = q[0]
        if len(q)>1:
          gene       = q[1]
          ko         = q[2].strip()
          systematic_to_gene[organism_name][systematic] = gene
          systematic_to_ko[organism_name][systematic]   = ko
      f.close()

      for my_systematic in systematic_to_ko[organism_name].keys():
        if systematic_to_ko[organism_name][my_systematic] in KOs_in_original_hierarchy:
          systematic_in_hierarchy[organism_name].add(my_systematic)
    
    # read file KO_gene_hierarchy_changes.csv containing genes to be added to the hierarchy
    # update the dictionaries 'systematic_to_gene' and 'systematic_to_ko' and 'systematic_in_hierarchy'
    
    my_added_ko = {}

    f = open(pp.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()
    for line in igot:
      q = re.split("\t",line.strip())
      my_organism   = q[0]
      my_systematic = q[1]
      my_gene       = q[2]
      my_gene       = re.split(', ',my_gene)
      my_gene       = my_gene[0]
      my_ko         = q[3]
      my_pathway    = q[4]
      if len(my_ko) == 0:
        my_ko = my_organism + "_" + my_systematic
      if my_organism in systematic_to_gene:
        systematic_to_gene[my_organism][my_systematic] = my_gene
        systematic_to_ko[my_organism][my_systematic]   = my_ko
        if len(my_pathway)>0:
          systematic_in_hierarchy[my_organism].add(my_systematic)
    f.close()
            
    self.systematic_to_gene = systematic_to_gene
    self.systematic_to_ko   = systematic_to_ko
    self.systematic_in_hierarchy = systematic_in_hierarchy


  def get_protein_lengths(self,my_organism,standard_length):
    
    # reads file with protein lengths
    # returns dictionary protein names -> protein lengths
    # standard_length == 0: do not insert standard length

    ffi = open(self.pp.get_protein_length_file(my_organism))
    igot = ffi.readlines()
    prot_to_length = {}
    for line in igot:
      tt = re.split("\t",line.strip())
      my_prot = tt[0]
      if len(tt)>3:
        my_length = float(tt[3])
      else:
        if not(standard_length ==0):
          my_length = standard_length
      prot_to_length[my_prot] = my_length
    return prot_to_length


  def get_pathways_in_original_hierarchy(self):
    # read list of pathways appearing in the original hierarchy file
    fi = open(self.pp.INFILE_KO_HIERARCHY_FILE, 'r')
    igot = fi.readlines()
    pathways_in_hierarchy = []
    for line in igot:
      if not(line[0:3] == "\t\t\t"):
        pathways_in_hierarchy.append(line[2:].strip())
    return pathways_in_hierarchy


  def get_mapping_systematic_to_ko_gene(self,my_organism,my_added_ko):

    mapping_files = self.pp.get_mapping_files(my_organism)

    # make dictionary 'systematic_to_ko_gene' with mapping
    # from systematic gene names to ko and gene name
    systematic_to_ko_gene = {}
    
    # data from original mapping file (from KEGG)
    fi = open(mapping_files['original'],"r")
    igot = fi.readlines()
    for line in igot:
      q = re.split('\t', line.strip())
      my_ko         = q[2]
      my_gene       = q[1]
      my_systematic = q[0]
      systematic_to_ko_gene[my_systematic] = {"ko": my_ko, "gene": my_gene}
    fi.close()
    
    # include entries from annotation changes file
    for added_ko in my_added_ko:
      if added_ko["organism"] == my_organism:
        my_ko   = added_ko["ko"]
        my_gene = added_ko["gene"]
        my_systematic = added_ko["systematic"]
        systematic_to_ko_gene[my_systematic] = {"ko": my_ko, "gene": my_gene}
    return systematic_to_ko_gene


  def get_ko_mapping_one(self,organism_list,relevant_ko):
    # for each organism: one dictionary for the mapping between ko numbers and genes
    ko_to_genes = {}
    for organism_name in organism_list:
      ko_to_genes[organism_name] = {}
      mapping_files = self.pp.get_mapping_files(organism_name)
      f = open(mapping_files['standardised'], 'r')
      igot = f.readlines()        
      for line in igot:
        q     = re.split('\t', line)
        ko    = q[0]
        genes = q[1].strip()
        ko_to_genes[organism_name][ko] = genes
      f.close()
    return ko_to_genes


  def get_ko_mappings(self,organism_list,relevant_ko):
    # Returns  dictionaries for the mapping between ko numbers and gene names
    # (each of them contains dictionaries for all organisms)
    #   ko_to_genes
    #   ko_to_orfs
    #   genes_to_ko
    #   systematic_to_ko
    #   ko_to_genes_completed
    #   ko_to_orfs_completed

    ko_to_genes      = {}
    ko_to_orfs       = {}
    genes_to_ko      = {}
    systematic_to_ko = {}

    for organism_name in organism_list:
      my_ko_to_genes = {}
      my_ko_to_orfs  = {}
      my_genes_to_ko = {}
      my_systematic_to_ko  = {}
      mapping_files = self.pp.get_mapping_files(organism_name)
      fh = open(mapping_files['original'],"r")
      igot = fh.readlines()        
      for line in igot:
        q = re.split('\t', line.strip())
        if len(q) > 1:
          ko   = q[2]
          if ko in relevant_ko:
            gene = q[1]
            orf  = q[0]
            if not ko in my_ko_to_genes:
              my_ko_to_genes[ko] = [gene]
            else:
              my_ko_to_genes[ko].append(gene)
            if not ko in my_ko_to_orfs:
              my_ko_to_orfs[ko] = [orf]
            else:
              my_ko_to_orfs[ko].append(orf)
      fh.close()
    
      my_systematic_to_ko = {}
      my_genes_to_ko      = {}
      
      for my_ko in my_ko_to_genes:
        my_ko_to_genes[my_ko] = list(set(my_ko_to_genes[my_ko]))
        for my_gene in my_ko_to_genes[my_ko]:
          my_genes_to_ko[my_gene] = my_ko
              
      for my_ko in my_ko_to_orfs:
        my_ko_to_orfs[my_ko] = list(set(my_ko_to_orfs[my_ko]))
        for my_orf in my_ko_to_orfs[my_ko]:
          my_systematic_to_ko[my_orf] = my_ko

      ko_to_genes[organism_name]      = my_ko_to_genes
      ko_to_orfs[organism_name]       = my_ko_to_orfs
      genes_to_ko[organism_name]      = my_genes_to_ko
      systematic_to_ko[organism_name] = my_systematic_to_ko

    f = open(self.pp.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()
    for line in igot:
      q = re.split("\t",line.strip())
      my_organism   = q[0]
      my_systematic = q[1]
      my_gene       = q[2]
      my_gene       = re.split(', ',my_gene)
      my_gene       = my_gene[0]
      my_ko         = q[3]
      if len(my_ko) == 0:
        my_ko = my_organism + "_" + my_systematic
      if my_organism in ko_to_genes:
        if my_gene in genes_to_ko[my_organism]:
          ko_remove = genes_to_ko[my_organism][my_gene]
          while my_gene in ko_to_genes[my_organism][ko_remove]:
            ko_to_genes[my_organism][ko_remove].remove(my_gene)
          while my_systematic in ko_to_orfs[my_organism][ko_remove]:
            ko_to_orfs[my_organism][ko_remove].remove(my_systematic)
        if my_ko in ko_to_genes[my_organism]:
          ko_to_genes[my_organism][my_ko].append(my_gene)
          ko_to_orfs[my_organism][my_ko].append(my_systematic)
        else:
          ko_to_genes[my_organism][my_ko] = [my_gene]
          ko_to_orfs[my_organism][my_ko]  = [my_systematic]
    
    f.close()

    ## make ko to gene lists, complete names of missing genes by "" 
    
    ko_to_genes_completed = {};
    ko_to_orfs_completed  = {};
    
    for organism_name in organism_list:
      ko_to_genes_completed[organism_name] = {}
      ko_to_orfs_completed[organism_name] = {}
      for my_ko in relevant_ko:
        if my_ko in ko_to_genes[organism_name]:
          gene_string = ''
          for lll in list(set(ko_to_genes[organism_name][my_ko])):
            gene_string = gene_string + " " + lll
          gene_string = gene_string.strip()
          ko_to_genes_completed[organism_name][my_ko] = gene_string
          orf_string = ''
          for lll in list(set(ko_to_orfs[organism_name][my_ko])):
            orf_string = orf_string + " " + lll
          orf_string = orf_string.strip()
          ko_to_orfs_completed[organism_name][my_ko] = orf_string
        else:
          ko_to_genes_completed[organism_name][my_ko] = "-"
          ko_to_orfs_completed[organism_name][my_ko] = "-"

    return ko_to_genes, ko_to_orfs, genes_to_ko, systematic_to_ko, ko_to_genes_completed, ko_to_orfs_completed


  def get_ko_to_category(self,organism_list):
    # for each organism:
    # mapping from ko numbers to categories
    ko_to_category = {}
    for organism_name in organism_list:
        infile = self.pp.DATA_DIR + "/hierarchy/" + organism_name + "_hierarchy_standardised.tms"
        fi     = open(infile, 'r')
        igot   = fi.readlines()
        for line in igot:
          if line[3] == '\t':
            my_ko = line.strip()
            ko_to_category[my_ko] = my_category
          else:
            if line[2] == '\t':
              my_category = line.strip()
    return ko_to_category


#########################################################################


class relevant_ko:

  def __init__(self,data_dir):
    self.pp = proteomaps_path_names(data_dir)
    self.INFILE_ANNOTATION_CHANGES = self.pp.INFILE_ANNOTATION_CHANGES  


  def get_added_ko(self):    
    # list of additional ko numbers (from annotation changes file)
    # if no ko number is given, invent one from organism name and systematic gene name
    
    f = open(self.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()
    my_added_ko = []
    for line in igot:
      q = re.split("\t",line.strip())
      my_organism   = q[0]
      my_systematic = q[1]
      my_ko         = q[3]
      if len(my_ko) == 0:
          my_ko = my_organism + "_" + my_systematic
      if not(my_ko in my_added_ko):
        my_added_ko.append(my_ko)
    f.close()
    return my_added_ko


  def get_added_ko_dictionary(self):
    # list of additional ko numbers (from annotation changes file)
    # each entry is a dictionary with entries 'organism'; 'systematic'; 'gene'; 'ko';
    # if no ko number is given, invent one from organism name and systematic gene name
    f = open(self.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()    
    my_added_ko = []
    for line in igot:
        q = re.split("\t",line.strip())
        my_organism = q[0]
        my_systematic = q[1]
        my_gene = q[2]
        my_gene = re.split(', ',my_gene)
        my_gene = my_gene[0]
        my_ko = q[3]
        if my_ko == "":
          my_ko = my_organism + "_" + my_systematic
        my_added_ko.append({"organism": my_organism, "systematic": my_systematic, "gene": my_gene,"ko": my_ko})
    f.close()
    return my_added_ko


  def get_added_ko_2(self,pathways_in_hierarchy):
    # more elaborate version of get_added_ko, needed for some purposes
    added_ko_2_pathway  = {}
    
    f    = open(self.pp.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()
    for line in igot:
        q = re.split("\t",line.strip())
        my_organism   = q[0]
        my_systematic = q[1]
        my_ko         = q[3]
        if len(my_ko) == 0:
            my_ko = my_organism + "_" + my_systematic
        my_pathway  = q[4]
        if my_organism in self.pp.get_organism_list():
            if my_pathway in pathways_in_hierarchy:
                added_ko_2_pathway[my_ko] = my_pathway
    f.close()
    
    all_added_ko = added_ko_2_pathway.keys()
    
    my_added_ko  = {}
    
    for my_ko in added_ko_2_pathway:
        my_pathway = added_ko_2_pathway[my_ko]
        if my_pathway in my_added_ko:
            my_added_ko[my_pathway].append(my_ko)
        else:
            my_added_ko[my_pathway] = [my_ko]
    return my_added_ko, all_added_ko


  def all_relevant_ko(self):
    # (set of) all ko numbers that appear in annotation changes file or data files
    collected_ko     = set(self.get_added_ko())
    data_files_ko    = self.pp.get_data_files_2()
    for data_file_triple in data_files_ko:
      fh   = open(data_file_triple[0],"r")
      igot = fh.readlines()
      for line in igot:
        q    = re.split('\t', line.strip())
        gene = q[0]
        ko   = q[1]
        collected_ko = collected_ko.union([ko])
    return collected_ko


  def write_relevant_ko(self,collected_ko,file_relevant_ko):
    # write prepared list of relevant ko numbers to file pp.FILE_RELEVANT_KO
    f = open(file_relevant_ko, 'w')
    for my_ko in list(collected_ko):
        f.write(my_ko+"\n")
    f.write("NotMapped\n")


  def read_relevant_ko(self,file_relevant_ko):
    # read prepared list of relevant ko numbers from file pp.FILE_RELEVANT_KO
    relevant_ko = []
    f = open(file_relevant_ko, 'r')
    igot = f.readlines()
    for line in igot:
        q = line.strip()
        relevant_ko.append(q)
    return relevant_ko
