import re
import os
from proteomaps_PATHNAMES import proteomaps_PATHNAMES

class proteomaps_path_names:

  def __init__(self,data_dir,hierarchy_version):

    a = proteomaps_PATHNAMES(hierarchy_version)

    # Predefined directory names
    self.PROTEIN_HIERARCHY_DIR = a.PROTEIN_HIERARCHY_DIR
    self.PROTEIN_LENGTH_DIR    = a.PROTEIN_LENGTH_DIR
    self.TMP_DIR               = a.TMP_DIR
    
    # Files defining the functional hierarchy
    self.INFILE_KO_HIERARCHY_FILE    = a.INFILE_KO_HIERARCHY_FILE
    self.INFILE_ANNOTATION_CHANGES   = a.INFILE_ANNOTATION_CHANGES
    self.INDIR_ORGANISM_MAPPING      = a.INDIR_ORGANISM_MAPPING

    # Determined from predefined names and "data_dir"
    self.DATA_DIR                    = data_dir
    self.OUTDIR_HIERARCHY            = data_dir + "/hierarchy/"
    self.OUTDIR_TABLES               = data_dir + "/tables/"
    self.INFILE_FILENAMES            = data_dir + "/filenames.csv"
    self.FILE_RELEVANT_KO            = data_dir + "/hierarchy/KO_relevant.csv"
    self.OUTFILE_KO_HIERARCHY_FILE_1 = data_dir + "/hierarchy/KO_hierarchy_standardised.tms"
    self.OUTFILE_KO_HIERARCHY_FILE_2 = data_dir + "/hierarchy/KO_hierarchy_standardised_pos.tms"
    self.OUTFILE_KO_HIERARCHY_FILE_3 = data_dir + "/hierarchy/KO_hierarchy_standardised_SomeNonMapped.tms"
    self.OUTFILE_KO_COLOR_FILE       = data_dir + "/hierarchy/KO_color_table.csv"

    # determine 'data_files' and 'organism_list' (to be given read through methods)
    data_files    = []
    organism_list = set()
    f = open(self.INFILE_FILENAMES,'r')
    igot = f.readlines()
    for line in igot:
      q = re.split('\t', line.strip())
      data_files.append([q[1],q[0],q[2]])
      organism_list.add(q[0])
    self.data_files    = data_files
    self.organism_list = list(organism_list)

  def get_organism_list(self):
    return self.organism_list

  def get_protein_length_file(self,my_organism):
    protein_length_file = self.PROTEIN_LENGTH_DIR + "/" + my_organism + "_protein_lengths.csv"
    return protein_length_file
    
  def get_filenames(self,data_file_triple):
    # return filenames (dict) for proteomaps workflow
    
    filenames   = {}
    my_organism = data_file_triple[1]
    my_data_set = data_file_triple[2]
    dum         = re.split('/',data_file_triple[0])
    filenames_short = dum[-1]
    if filenames_short[-4:] == ".txt" or filenames_short[-4:] == ".csv":
      filenames_short = filenames_short[:-4] + ".csv"
    path = self.DATA_DIR + "/" + data_file_triple[2]
    filenames['organism']                  = my_organism
    filenames['data_set']                  = my_data_set
    filenames['short']                     = filenames_short
    filenames['original_data']             = data_file_triple[0]
    filenames['abundance']                 = path + '/' + my_organism + "_abundance_" + filenames_short
    filenames['cost']                      = path + '/' + my_organism + "_cost_" + filenames_short
    filenames['ko']                        = path + '/' + my_organism + "_ko_"   + filenames_short
    filenames['cost_lumped_proteins']      = path + '/' + my_organism + "_cost_NonMappedLumpedProteins_" + filenames_short
    filenames['abundance_lumped_proteins'] = path + '/' + my_organism + "_abundance_NonMappedLumpedProteins_" + filenames_short
    filenames['nonmapped']                 = path + '/' + my_data_set + "_non_mapped.csv"
    # final versions of value, mapping and hierarchy files,
    # where some non-mapped proteins are merged into a lumped "Other unmapped"
    filenames['abundance_lumped']           = path + '/' + my_organism + "_values_abundance_lumped_" + filenames_short
    filenames['cost_lumped']                = path + '/' + my_organism + "_values_cost_lumped_" + filenames_short
    filenames['mapping_abundance_lumped']   = path + '/' + my_data_set + "_mapping_abundance_lumped.csv"
    filenames['mapping_cost_lumped']        = path + '/' + my_data_set + "_mapping_cost_lumped.csv"
    filenames['hierarchy_abundance_lumped'] = path + '/' + my_data_set + "_hierarchy_abundance_lumped.tms"
    filenames['hierarchy_cost_lumped']      = path + '/' + my_data_set + "_hierarchy_cost_lumped.tms"
    filenames['hierarchy_abundance_lumped_pos'] = path + '/' + my_data_set + "_hierarchy_abundance_lumped_pos.tms"
    filenames['hierarchy_cost_lumped_pos']      = path + '/' + my_data_set + "_hierarchy_cost_lumped_pos.tms"
    filenames['processed_data']                 = path + '/' + my_data_set + ".csv"
    return filenames

  def get_data_files(self):
    # read "filenames.csv" files and return its contents as a data structure:
    # list of triples:
    # [original file name, organism code, data directory]
    return self.data_files

  def get_data_files_2(self):
    # read "filenames.csv" files and return its contents as a data structure
    # list of triples:
    # [processed data file with ko numbers, organism code, processed data file]

    data_files = []
    f = open(self.INFILE_FILENAMES,'r')
    igot = f.readlines()
    for line in igot:
      q = re.split('\t', line.strip())
      dum = re.split('/',q[1])
      q[1] = dum[-1]
      data_files.append([self.DATA_DIR + '/' + q[2] + '/' + q[0] + '_ko_' + q[1],q[0],q[2]])
    return data_files

  def make_data_file_directories(self):    
    # Create directories if they do not exist
    
    path = self.OUTDIR_HIERARCHY
    if not os.path.isdir(path):
      os.mkdir(path)
      print 'Making directory ' + path
    path = self.OUTDIR_TABLES
    if not os.path.isdir(path):
      os.mkdir(path)
      print 'Making directory ' + path
    for data_file in self.data_files:
      path = self.DATA_DIR + '/' + data_file[2]
      if not os.path.isdir(path):
        os.mkdir(path)
        print 'Making directory ' + path


  def get_mapping_files(self, organism_name):
    # Return filenames for all mapping files (for given organism)
    
    path = self.DATA_DIR + "/hierarchy/"
    mapping_filenames = {}
    mapping_filenames['original']              = self.INDIR_ORGANISM_MAPPING + "/" + organism_name + "_mapping.csv"
    mapping_filenames['standardised']          = path + organism_name + "_mapping_standardised.csv"
    mapping_filenames['standardised_genepair'] = path + organism_name + "_mapping_standardised_genepair.csv"
    mapping_filenames['standardised_pair']     = path + organism_name + "_mapping_standardised_pair.csv"
    mapping_filenames['final']                 = path + organism_name + "_mapping_final.csv"
    mapping_filenames['final_some_unmapped']   = path + organism_name + "_mapping_final_some_unmapped.csv"
    return mapping_filenames
