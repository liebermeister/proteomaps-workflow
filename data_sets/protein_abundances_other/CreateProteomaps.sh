# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_other /home/wolfram/Proteomaps/data_paver_input/data_for_paver_other 10 KO_gene_hierarchy_2014-08-01

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_other KO_gene_hierarchy_2014-08-01
