import re
import os
from proteomaps_path_names import proteomaps_path_names

# -----------------------------------------------------

class relevant_ko:

  def __init__(self,data_dir,pp):
    self.pp = pp
    #self.pp = proteomaps_path_names(data_dir)
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
    # list of additional ko numbers (from annotation changes file)

    added_ko_2_pathway  = {}
    
    f    = open(self.pp.INFILE_ANNOTATION_CHANGES, 'r')
    igot = f.readlines()
    for line in igot:
        q = re.split("\t",line.strip())
        my_organism   = q[0]
        my_systematic = q[1]
        my_ko         = q[3]
        my_pathway    = q[4]
        if len(q)>5:
          my_comment    = q[5]
        else:
          my_comment    = ""
        if len(my_ko) == 0:
            my_ko = my_organism + "_" + my_systematic
        if my_organism in self.pp.get_organism_list():
            if my_pathway in pathways_in_hierarchy:
                added_ko_2_pathway[my_ko] = my_pathway
        elif not(my_comment[0:16]=="KEGG web services"):
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
