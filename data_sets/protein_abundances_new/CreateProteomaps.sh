# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_new /home/wolfram/Proteomaps/data_paver_input/data_for_paver_new 10 KO_gene_hierarchy_2014-08-01

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_new KO_gene_hierarchy_2014-08-01
