# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_mouse /home/wolfram/Proteomaps/data_paver_input/data_for_paver_geiger_mouse 10 KO_gene_hierarchy_2014-08-01

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_geiger_mouse KO_gene_hierarchy_2014-08-01

