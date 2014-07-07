# Run python script for creating proteomaps 

cd /home/wolfram/Proteomaps/python/

python CreateProteomaps.py /home/wolfram/Proteomaps/data_sets/protein_abundances_paper /home/wolfram/Proteomaps/data_paver_input/data_for_paver_paper 10

python CreateRectangular.py /home/wolfram/Proteomaps/data_sets/protein_abundances_paper

# ------------------------------------------------------------
# run only the last two scripts

cd /home/wolfram/Proteomaps/python/proteomaps_workflow
python prune_nonmapped_proteins.py ~/Proteomaps/data_sets/protein_abundances_paper/
python prepare_files_for_paver.py ~/Proteomaps/data_sets/protein_abundances_paper/ ~/Proteomaps/data_paver_input/data_for_paver_paper/
