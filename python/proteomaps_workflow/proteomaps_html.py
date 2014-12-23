# --------------------------------------------------------------------------------
# Translate html pages written by Paver into html pages used in proteomaps website
# --------------------------------------------------------------------------------

import csv
import sys
import os
import re
import math

from HTMLParser import HTMLParser
from proteomaps_PATHNAMES import proteomaps_PATHNAMES


# ======================================================================================

class MyHTMLParser(HTMLParser):
    """
    my HTML parser for collecting the content of area tags
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        
    def handle_starttag(self,tag,attrs):
        if tag =='area':
            my_area_tag = {}
            for attr in attrs:
                my_area_tag[attr[0]] = attr[1]
            self.data.append(my_area_tag)

# ======================================================================================

def to_precision(x,p):
    """
    returns a string representation of x formatted with a precision of p
    see http://randlet.com/blog/python-significant-figures-format/

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)


# ======================================================================================
# load amount data

class mapping_from_file:

    def __init__(self, mapping_file):
        # print mapping_file
        mapping = {}        
        file = open(mapping_file,'r')
        igot = file.readlines()
        for line in igot:
            q = re.split('\t', line.strip())
            if len(q)>1:
                my_key = q[0]
                my_value = q[1]
                mapping[my_key] = my_value
        self.mapping = mapping


# ======================================================================================
class gene_mapping_file:

    def __init__(self, mapping_file):

        # print mapping_file
        mapping = {}        
        file = open(mapping_file,'r')
        igot = file.readlines()
        for line in igot:
            q = re.split('\t', line.strip())
            r = re.split(':', q[1])
            my_KO = q[0]
            my_gene = r[0]
            my_systematic = r[1] 
            mapping[my_systematic] = my_gene
        self.mapping = mapping

# ======================================================================================

class proteomap_make_one_html_file:

    """
    class for making an HTML file based on paver html output
    """
    
    def __init__(self, html_input_file, picture_file, organism, mapping_file, resolution_1, resolution_2, amount_file, weighted_amount_file, article_name, level, data_set_name, flag_zoom, data_type,picture_format):

        """
        Arguments:
         html_input_file   html file produced by paver (full path)
         picture_file      proteomaps graphics file (without path)
         organism:         string (kegg organism name)
         mapping_file:     final processed mapping file (name .._mapping_final_some_unmapped.csv)  (full path)
         resolution_1:     resolution of original picture (from paver)
         resolution_2:     size of the picture as shown on the website
         amount_file:      data file with (non-mass weighted) protein abundances (full path)
         weighted_amount_file: data file with (mass weighted) protein abundances (full path)
         article_name:     string (name of paper)
         level:            string denoting the proteomaps level ('lv1','lv2','lv3','lv5')
         data_set_name     short name of data set (as given in [data_dir]/filenames.csv and used in filenames)
         flag_zoom:        1: page with zoom effect / 0: page without toom effect
         data_type:        'cost' or 'abundance'
         picture_format:   'jpg' or 'png'
        """

        a = proteomaps_PATHNAMES()
        self.PROTEIN_HIERARCHY_DIR = a.PROTEIN_HIERARCHY_DIR

        # precompute some mappings
        self.tag_to_amount = mapping_from_file(amount_file).mapping
        self.tag_to_weighted_amount = mapping_from_file(weighted_amount_file).mapping
        self.id_to_gene     = gene_mapping_file(mapping_file).mapping
        self.data_type      = data_type
        self.picture_format = picture_format
        
        # mapping id -> kegg_id
        if organism == 'hsa':
            hsa_kegg_mapping_file = self.PROTEIN_HIERARCHY_DIR + "/KO_gene_hierarchy_organism_mapping/hsa_uniprot_to_GeneID.csv"
            self.id_to_kegg_id = mapping_from_file(hsa_kegg_mapping_file).mapping
        else:
            self.id_to_kegg_id = {}
            for my_id in self.id_to_gene:
                self.id_to_kegg_id[my_id] = my_id

        # make header, map, and footer parts of html file
        self.header = self.get_header(picture_file, organism, mapping_file, article_name, level, data_set_name, flag_zoom)
        self.map_tag = self.get_map_tag(html_input_file, organism, resolution_1, resolution_2, level)
        self.footer = ['  </body>','</html>']


    def get_header(self, picture_file, organism, mapping_file, article_name, level, data_set_name,flag_zoom):

        preload_file = data_set_name + '_preloadImages.js'

        picture_file_800 = picture_file[:-4] + "_800.png"
        header = []
        header.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">')
        header.append('<html>')
        header.append('  <head>')
        header.append('    <title>Protein abundances</title>')
        header.append('    <link rel="stylesheet" type="text/css" href="../../proteomaps.css">')
        if flag_zoom ==1:
            header.append('    <script src="../../shiftzoom.js" language="javascript" type="text/javascript"></script>')
        header.append("");
        header.append("    <script>");
        header.append("     (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){");
        header.append("     (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),");
        header.append("     m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)");
        header.append("     })(window,document,'script','//www.google-analytics.com/analytics.js','ga');");
        header.append("     ga('create', 'UA-4526009-11', 'proteomaps.net');");
        header.append("     ga('send', 'pageview');");
        header.append('    </script>');
        header.append("");
        header.append('    <script src="' + preload_file + '"></script>');
        header.append("");
        header.append('  </head>')
        header.append("");
        header.append('  <body>')
        header.append('  <table><tr><td></td><td>')

        header.append('  <p style="font-size:14; width:2000; height:20;"> ' + article_name + '&nbsp;&nbsp;')

        if flag_zoom == 1:
            if self.data_type == "cost":
                header.append('  Mass-weighted&nbsp; <a href="' + data_set_name + '_abundance.html">[Copy numbers]</a>')
            elif self.data_type == "abundance":
                header.append('  <a href="' + data_set_name + '_cost.html">[Mass-weighted]</a> Copy numbers&nbsp;')
        else:
            if self.data_type == "cost":
                header.append('  Mass-weighted&nbsp; <a href="' + data_set_name + '_abundance_' + level + '.html">[Copy numbers]</a>')
            elif self.data_type == "abundance":
                header.append('  <a href="' + data_set_name + '_cost_' + level + '.html">[Mass-weighted]</a> Copy numbers&nbsp;')
        header.append('&nbsp;&nbsp;')

        if level == 'lv1':
            header.append('  < | 1')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv2.html">2</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv3.html">3</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv5.html">4</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv2.html">></a>')
            header.append('&nbsp;&nbsp;')
            header.append('  <a href="'   + data_set_name + '_' + self.data_type +'.html">[Zoom]</a>')

        if level == 'lv2':
            header.append('  ')
            header.append('  <a href="' + data_set_name + '_' + self.data_type +'_lv1.html"><</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv1.html">1</a>')
            header.append('  | 2')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv3.html">3</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv5.html">4</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv3.html">></a>')
            header.append('&nbsp;&nbsp;')
            header.append('  <a href="' + data_set_name + '_' + self.data_type +'.html">[Zoom]</a>')

        if level == 'lv3':
            header.append('  ')
            header.append('  <a href="' + data_set_name + '_' + self.data_type +'_lv2.html"><</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv1.html">1</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv2.html">2</a>')
            header.append('  | 3')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv5.html">4</a>')
            header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv5.html">></a>')
            header.append('&nbsp;&nbsp;')
            header.append('  <a href="' + data_set_name + '_' + self.data_type +'.html">[Zoom]</a>')

        if level == 'lv5':
            if flag_zoom == 1:
                header.append('  ')
                header.append('  <')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv1.html">1</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv2.html">2</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv3.html">3</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv5.html">4</a>')
                header.append('  | > &nbsp;&nbsp;&nbsp;')
                header.append('  Zoom')
            else:
                header.append('  ')
                header.append('  <a href="' + data_set_name + '_' + self.data_type +'_lv3.html"><</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv1.html">1</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv2.html">2</a>')
                header.append('  | <a href="' + data_set_name + '_' + self.data_type +'_lv3.html">3</a>')
                header.append('  | 4')
                header.append('  | > &nbsp;&nbsp;')
                header.append('  <a href="' + data_set_name + '_' + self.data_type +'.html">[Zoom]</a>')

        header.append('  </p></td></tr>')
        header.append('  <tr> ')
        header.append('    <td style = "vertical-align: top;"><img class="wrap" width ="40" src="../../pictures/proteomaps_label.jpg"></td>')
        
        if flag_zoom == 1:
            header.append('    <td><div><img class="shiftzoom" onLoad="shiftzoom.add(this,{showcoords:false,relativecoords:true,wheelstep:40,millisec:1,wheelinvert:true});" src="./pictures/' +  picture_file + '" width="800"></div></td>')            
        else:
            header.append('  <td><div><img src="./pictures/' + picture_file_800 + '" align="left" usemap="\#proteins" class="wrap" width="800"></div></td>')
        
        header.append('  </tr>')
        header.append('  <tr><td></td><td><p><a href="./pictures/' + picture_file + '"  download="' + picture_file + '">[Download image]</a>&nbsp;&nbsp;')
        header.append('  <a href="../../index.html">[Home]</a>&nbsp;&nbsp;')
        header.append('  <a href="../../help.html" target="_blank">[Help]</a></p></td></tr>')

        header.append('  </td></tr></table>')
        return header

    def write_file(self, output_file):
            
        print 'Writing file ' + output_file
        fo = open(output_file,'w')
        for line in self.header:
            fo.write(line + '\n')
        for line in self.map_tag:
            fo.write(line + '\n')
        for line in self.footer:
            fo.write(line + '\n')
        fo.close

    def scale_to_total_protein_molecule_number(self, organism, amount_fraction):

        # see Ron's numbers (email 25/09/13)
        total_protein_numbers = {'mpn': 50000, 'eco': 3000000, 'syn': 3000000, 'sce': 100000000, 'spo': 300000000, 'ath': 10000000000, 'dme': 10000000000, 'mmu': 10000000000, 'hsa': 10000000000}

        protein_number = total_protein_numbers[organism] * amount_fraction
        if protein_number >= 100000:
            protein_number = '%s' % int(round(float('%.2g' % protein_number)))
            exponent_num  = int(math.floor(math.log10(float(protein_number))))
            prefactor_num = float(protein_number)/float(10**exponent_num)
            exponent  = '%s' % int(round(float('%.2g' % exponent_num)))
            prefactor = '%s' % float('%.2g' % prefactor_num)
            protein_number = prefactor + " * 10^" + exponent
        else:
            protein_number = '%s' % int(round(float('%.2g' % protein_number)))
        return protein_number
    
    def get_map_tag(self, html_input_file, organism, resolution_1, resolution_2, level):

        map_tag = ['    <map name="proteins">']

        if level == 'lv5':
            url_string = 'http://www.genome.jp/dbget-bin/www_bget?' + organism + ':'
        else:
            url_string = ''

        try:
            file = open(html_input_file ,'r')
        except:
            print "File " + html_input_file + " not found; the html page will have no tooltips"
            map_tag = ['    <map name="proteins"></map>']
            return map_tag
        html_text = file.read()
        file.close()
        parser = MyHTMLParser()
        parser.feed(html_text)
        area_tags = parser.data
        
        for areaTag in area_tags:
            my_name   = areaTag['alt']
            my_coords = areaTag['coords']

            coords_list = re.split(',', my_coords)
            new_coords = ''
            for coord in coords_list:
                new_coords = new_coords + str(int(float(resolution_2) / float(resolution_1) * float(coord))) + ','

            url_term = ''

            if level == 'lv5':
                if my_name in self.id_to_kegg_id:
                    my_kegg_id = self.id_to_kegg_id[my_name]
                else:
                    my_kegg_id = ''
    
                if my_name in self.id_to_gene:
                    my_gene = self.id_to_gene[my_name]
                    my_name_string = my_gene + ' [' + my_name + ']'
                else:
                    my_name_string = my_name
                
                if len(url_string) * len(my_kegg_id) > 0:
                    url_term = ' href="' + url_string + my_kegg_id + '" target="_blank"'
            else:
                my_name_string = my_name

            if my_name in self.tag_to_weighted_amount:
                amount_fraction = float(self.tag_to_amount[my_name])
                est_copy_number = self.scale_to_total_protein_molecule_number(organism, amount_fraction)
                my_amount = 'Estimated copy number: ~ ' + est_copy_number
                my_amount = my_amount + '\nFraction by copy number:' + to_precision(float(100.00 * float(self.tag_to_amount[my_name])),2) + ' percent'
                my_amount = my_amount + '\nFraction by mass:' + to_precision(float(100.00 * float(self.tag_to_weighted_amount[my_name])),2) + ' percent'
            else:
                my_amount = ''

            map_tag.append('       <area shape="poly" coords="' + new_coords + '" alt="' + my_name + '" title="' + my_name_string + "\n" + my_amount + '"' + url_term + '>')
        
        map_tag.append("     </map>")
        
        return map_tag
    
# ======================================================================================

class proteomap_process_html:

    def __init__(self, paver_html_dir, html_dir, data_dir, data_set_name, organism, resolution_1, resolution_2,article_name,data_type,picture_format="jpg"):

        """
        Arguments:
         paver_html_dir:   directory with html files produced by paver
         html_dir:         output directory for new html files
         data_dir:         directory in which the data sets are defined
         data_set_name     short name of data set (as given in [data_dir]/filenames.csv and used in filenames)
         organism:         string (kegg organism name)
         resolution_1:     resolution of original picture (from paver)
         resolution_2:     size of the picture as shown on the website
         article_name:     string (name of paper)
         data_type:        'cost' or 'abundance'
         picture_format:   'jpg' or 'png'
        """
        
        levels = ['lv1','lv2','lv3','lv5']
        mapping_file = data_dir + "/hierarchy/" + organism + '_mapping_final_some_unmapped.csv'

        # make html pages for the four layers
        for level in levels:
            html_input_file       = paver_html_dir + '/' + data_set_name + '_' + data_type + '_' + level + '.html'
            picture_file          = data_set_name + '_' + data_type +'_' + level + '.' + picture_format
            amount_file           = data_dir + '/' + data_set_name + '/' + data_set_name + '_abundance_relative_' + level + '.csv'
            weighted_amount_file  = data_dir + '/' + data_set_name + '/' + data_set_name + '_cost_relative_' + level + '.csv'
            output_file           = html_dir + '/' + data_set_name + '_' + data_type +'_' + level + '.html'
            flag_zoom             = 0
            pm = proteomap_make_one_html_file(html_input_file, picture_file, organism, mapping_file, resolution_1, resolution_2, amount_file, weighted_amount_file, article_name,level,data_set_name,flag_zoom, data_type,picture_format)
            pm.write_file(output_file)

        # make html page with the zoom effect
        flag_zoom = 1
        pm_cost = proteomap_make_one_html_file(html_input_file, picture_file, organism, mapping_file, resolution_1, resolution_2, amount_file, weighted_amount_file,article_name,level,data_set_name,flag_zoom, data_type,picture_format)
        output_file  = html_dir + '/' + data_set_name + '_' + data_type +'.html'

        pm_cost.write_file(output_file)

        # make preload file

        preload = []
        preload.append('function preloader() {')
        preload.append('  if (document.images) {')
        preload.append('      var img1 = new Image();')
        preload.append('      var img2 = new Image();')
        preload.append('      var img3 = new Image();')
        preload.append('      var img4 = new Image();')
        preload.append('      var img5 = new Image();')
        preload.append('      var img6 = new Image();')
        preload.append('      var img7 = new Image();')
        preload.append('      var img8 = new Image();')
        preload.append('      img1.src = "./pictures/' + data_set_name + '_abundance_lv1_800.png";')
        preload.append('      img2.src = "./pictures/' + data_set_name + '_abundance_lv2_800.png";')
        preload.append('      img3.src = "./pictures/' + data_set_name + '_abundance_lv3_800.png";')
        preload.append('      img4.src = "./pictures/' + data_set_name + '_abundance_lv5_800.png";')
        preload.append('      img5.src = "./pictures/' + data_set_name + '_cost_lv1_800.png";')
        preload.append('      img6.src = "./pictures/' + data_set_name + '_cost_lv2_800.png";')
        preload.append('      img7.src = "./pictures/' + data_set_name + '_cost_lv3_800.png";')
        preload.append('      img8.src = "./pictures/' + data_set_name + '_cost_lv5_800.png";')
        preload.append("  }")
        preload.append("}")
        preload.append("function addLoadEvent(func) {")
        preload.append("  var oldonload = window.onload;")
        preload.append("  if (typeof window.onload != 'function') {")
        preload.append("    window.onload = func;")
        preload.append("  } else {")
        preload.append("    window.onload = function() {")
        preload.append("      if (oldonload) {")
        preload.append("        oldonload();")
        preload.append("      }")
        preload.append("      func();")
        preload.append("    }")
        preload.append("  }")
        preload.append("}")
        preload.append("addLoadEvent(preloader);")

        preload_file = html_dir + '/' + data_set_name + '_preloadImages.js'
        fo = open(preload_file,'w')
        for line in preload:
            fo.write(line + "\n")
        fo.close
        print "Writing file " + preload_file
        
# ======================================================================================

class make_proteomaps_html:

    def __init__(self, data_dir, html_dir, paver_html_dir, resolution_1, resolution_2, picture_format):
  
      """
      Create html pages for a data set bundle for proteomaps website
      
      Reads information about data sets from file filenames.csv in directory [data_dir]
      and creates html files for all data sets
      (calls the function proteomap_process_html in proteomaps_html)
  
      Arguments:
        data_dir:         directory in which the data sets are defined
        html_dir:         output directory for new html files
        paver_html_dir:   directory with html files produced by paver
        resolution_1:     resolution of original picture (from paver)
        resolution_2:     size of the picture as shown on the website
        picture_format:  'png' or 'jpg'
      """
      
      filenames_file = data_dir + "/filenames.csv"
      print "Data set directory: " + data_dir
  
      for row in csv.reader(open(filenames_file, 'r'), delimiter='\t'):
          organism, data_file, data_set_name, data_set_name_matlab, article_name = row
          print "\nData set " + data_set_name + ":\nWriting html files to directory " + html_dir

          data_type = "cost"
          proteomap_process_html(paver_html_dir, html_dir, data_dir, data_set_name, organism, resolution_1, resolution_2, article_name, data_type, picture_format)

          data_type = "abundance"
          proteomap_process_html(paver_html_dir, html_dir, data_dir, data_set_name, organism, resolution_1, resolution_2, article_name, data_type, picture_format)
