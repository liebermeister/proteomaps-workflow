# --------------------------------------------------------------
# Script for translating proteomap html pages written by Paver into
#  html pages for proteomaps website.
# Further information from the original data set directory is used
# The html pages are stored in some intermediate directory
# (use copy_files_to_website.py to later copy them to the web directory )
# --------------------------------------------------------------

from proteomaps_html import make_proteomaps_html 

## --------------------------------------------------------------
## data sets for paper 
#
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_paper/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_paper/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#
## --------------------------------------------------------------
## data set other 
# 
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_other/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_other/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#
## --------------------------------------------------------------
## Geiger's cell line data
#
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_cell_lines/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_geiger_cell_lines/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#  
## --------------------------------------------------------------
## Geiger's mouse tissue data
# 
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_mouse/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_geiger_mouse/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version) 
#
## --------------------------------------------------------------
## Valgepea E coli data
#
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_valgepea_ecoli/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_valgepea_ecoli/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#
## --------------------------------------------------------------
## data sets directory "new"
#
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_new/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_new/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#
## --------------------------------------------------------------
## synchechocystis 
#  
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_synechocystis/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_synechocystis/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
#
## --------------------------------------------------------------
## Khan Human / Chimpanzee data
#
#data_dir         = '/home/wolfram/Proteomaps/data_sets/protein_abundances_khan_human_chimp/'
#paver_html_dir   = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_khan_human_chimp/html/'
#output_html_dir  = '/home/wolfram/Proteomaps/data_html/'
#resolution_1     = 2512
#resolution_2     = 800
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
#
#make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
 
# --------------------------------------------------------------
# Small picture on main website
# 
# data_dir        = '/home/wolfram/Proteomaps/data_sets/protein_abundances_valgepea_ecoli/'
# paver_html_dir  = '/home/wolfram/Proteomaps/data_paver_output/proteomaps_valgepea_ecoli/html/'
# output_html_dir = '/home/wolfram/projekte/protein_abundance/html/MAKE_proteomaps_online/html_icon/'
# resolution_1    = 2512
# resolution_2    = 256
#hierarchy_version = 'KO_gene_hierarchy_2014-08-01'
# 
# make_proteomaps_html(data_dir, output_html_dir, paver_html_dir, resolution_1, resolution_2, 'png', hierarchy_version)
