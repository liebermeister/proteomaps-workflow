import os

class proteomaps_PATHNAMES:

  def __init__(self, hierarchy_version):

    # Base and tmp directory -- please edit
    self.BASE_DIR              = "/home/wolfram/Proteomaps/"
    self.TMP_DIR               = "/home/wolfram/tmp/matlab_protein_abundance";

    # Predefined directory names
    self.PROTEIN_HIERARCHY_DIR = self.BASE_DIR + "genomic_data/" + hierarchy_version + "/"
    self.PROTEIN_LENGTH_DIR    = self.PROTEIN_HIERARCHY_DIR + "protein_length_data/"

    # Files / subdirectories within the functional hierarchy
    self.INFILE_KO_HIERARCHY_FILE  = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy.tms"
    self.INFILE_ANNOTATION_CHANGES = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy_changes.csv"
    self.INDIR_ORGANISM_MAPPING    = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy_organism_mapping/"
    self.ORGANISM_INFORMATION      = self.PROTEIN_HIERARCHY_DIR + "/organisms.csv"

    # Python directory
    self.WORKFLOW_PATH = self.BASE_DIR + 'python/proteomaps_workflow/'
    self.MATLAB_PATH   = self.BASE_DIR + 'matlab/'
