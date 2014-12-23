import os

class proteomaps_PATHNAMES:

  def __init__(self):

    # Predefined directory names
    self.BASE_DIR              = "/home/wolfram/Proteomaps/"
    self.PROTEIN_HIERARCHY_DIR = "/home/wolfram/Proteomaps/genomic_data/KO_gene_hierarchy/"
    self.PROTEIN_LENGTH_DIR    = "/home/wolfram/Proteomaps/genomic_data/protein_length_data/"
    self.TMP_DIR               = "/home/wolfram/tmp/matlab_protein_abundance";

    # Files / subdirectories within the functional hierarchy
    self.INFILE_KO_HIERARCHY_FILE  = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy.tms"
    self.INFILE_ANNOTATION_CHANGES = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy_changes.csv"
    self.INDIR_ORGANISM_MAPPING    = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy_organism_mapping/"
    self.ORGANISM_INFORMATION      = self.PROTEIN_HIERARCHY_DIR + "/organisms.csv"

    # Python directory
    self.WORKFLOW_PATH = '/home/wolfram/Proteomaps/python/proteomaps_workflow/'
    self.MATLAB_PATH   = '/home/wolfram/Proteomaps/matlab/'
