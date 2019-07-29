# ----------------------------------------------------
# Class functions for proteomaps organism information
# Filenames are taken from class proteomaps_path_names
# ----------------------------------------------------

import re

# ----------------------------------------------

class proteomaps_organisms:

  def __init__(self,pn):
    self.organism_information_file = pn.ORGANISM_INFORMATION
    self.data = {}
    self.organisms = []
    
    fi = open(self.organism_information_file, 'r')
    igot = fi.readlines()
    for line in igot[2:]:
      [name,shortname,id_type,example_enolase,url,protsize] = re.split('\t',line.strip())
      #print name + " " + shortname + " " + id_type + " " + example_enolase + " " + url
      self.organisms.append(shortname)
      self.data[shortname] = {}
      self.data[shortname]['name'] = name
      self.data[shortname]['id_type'] = id_type
      self.data[shortname]['url'] = url
      self.data[shortname]['example_enolase'] = example_enolase
      self.data[shortname]['protsize'] = int(protsize)
      
#a = proteomaps_organisms()
#print a.organisms
#print a.data['mpn']
