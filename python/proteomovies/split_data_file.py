import os
import re
import sys
import argparse

# split_data_table.py
# 
# split data table into individual data files (one file for each column), as inputs for proteomaps workflow
# 
# Command line arguments
#
#   'data_set'    data set name
#   'infile'  path to input file
#   'outfile' path to output file
#   'organism'
#   'organism_long'
#   'data_set_long'
#
# Input file format
#
#   Two possible formats are supported:
#   
#   Format 1: simple table
#   
#   [IGNORED] [sample 1] [sample 2] ...
#   [gene 1]  value      value           ...
#   [gene 2]  value      value           ...
#   ...       ...        ...             ...
#   
#   Format 2: SBtab table
#   
#   !!SBtab .... [this line is ignored]
#   ![IGNORED] [sample 1] [sample 2] ...
#   [any further lines starting with ! are ignored]
#   [gene 1]   value      value      ...
#   [gene 2]   value      value      ...
#   ...        ...        ...        ...

def split_data_file(data_set,infile,outfile, organism, organism_long, data_set_long):

    infile_name, infile_extension = os.path.splitext(infile)
    if infile_extension == '.csv':
        delimiter = ","
    else:
        delimiter = '\t'

    input_file = open(infile,'r')
    igot = input_file.readlines()
    item = igot[0]
    if item[0:2]=='!!':
        item = igot[1]

    line = re.split(delimiter,item.strip())
    if len(line)<2:
        sys.exit("\nINVALID DATA FILE: The input data file must contain at least two tab-separated columns\n")
        
    conditions = line[1:]
    input_file.close()

    outfile_log = open(outfile + "_LOG.csv",'w')

    z = 0
    z_sample = 0
    for cond in conditions:
        z = z + 1
        if not(cond[0]=='!'):
            z_sample = z_sample + 1
            outfile_full = outfile + "_" + str(z_sample) + "_" + cond.replace(".","_") + ".csv"
            outfile_log.write(organism + "\t" + outfile_full +  "\t" + data_set + "_" + cond.replace(".","_") + "\t" + data_set_long + "\t" + organism_long + "\n")
            input_file  = open(infile,'r')
            output_file = open(outfile_full,'w')
            igot = input_file.readlines()
            if igot[0][0:2]=='!!':
                igot = igot[1:]
            for item in igot[1:]:
                line = re.split(delimiter,item.strip())
                gene = line[0]
                if not(gene[0]=='!'):
                    values = line[1:]
                    output_file.write(gene + "\t" + values[z-1] + '\n')
            input_file.close()
    outfile_log.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split proteomics csv table file into single-column files')
    parser.add_argument('data_set',    help='data set name')
    parser.add_argument('infile',  help='path to input file')
    parser.add_argument('outfile', help='path to output file')
    parser.add_argument('organism',help='organism shortname (three letters)')
    parser.add_argument('organism_long', help='organism name (in quotes)')
    parser.add_argument('data_set_long', help='data set long name (in quotes)')

    args = parser.parse_args()

    split_data_file(args.data_set, args.infile, args.outfile, args.organism, args.organism_long, args.data_set_long)
