# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_valgepea_ecoli /home/wolfram/Proteomaps/data_paver_input/data_for_paver_valgepea_ecoli 10 KO_gene_hierarchy_2014-08-01

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_valgepea_ecoli KO_gene_hierarchy_2014-08-01
