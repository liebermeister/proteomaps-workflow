# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_cell_lines /home/wolfram/Proteomaps/data_paver_input/data_for_paver_geiger_cell_lines 10 KO_gene_hierarchy_2014-08-01

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_cell_lines KO_gene_hierarchy_2014-08-01

