#!/usr/bin/Python 2.7

import sys
import os

# Set ariable for file
filename = sys.argv[1]

# Set counter to iterate over each line
count = 1

# Create lists to add values to eavh list
start_position = []
end_position = []
strand = []
gene = []
synonym = {}
# Read file
with open(filename, 'r') as f:
    for row in f.readlines()[3:]:
        line = row.split('\t')
        Location = line[0]
        Strand = line[1]
        Gene = line[4]
        Synonym = line[5]
        start_pos, end_pos = map(int, Location.split('..'))
        # print str(start_pos) + '\t' + str(end_pos)
        start_position.append(start_pos)
        end_position.append(end_pos)
        strand.append(Strand)
        gene.append(Gene)
        synonym[Gene] = Synonym
# print synonym
operon_list = []
while count < len(gene):
    prev_gene = gene[count - 1]
    curr_gene = gene[count]
    prev_start_pos = start_position[count - 1]
    curr_start_pos = start_position[count]
    prev_end_pos = end_position[count - 1]
    curr_end_pos = end_position[count]
    prev_strand = strand[count - 1]
    curr_strand = strand[count]
    if curr_strand == prev_strand:
        diff = abs(prev_end_pos - curr_start_pos)
        if diff < 50:
            operon_list.append(prev_gene)
            operon_list.append(curr_gene)
        else:
            if len(operon_list) > 0:
                for op in list(set(operon_list)):
                    sys.stdout.write("\t" + op + "\t" + synonym[op])
                print
            operon_list = []
    else:
        if len(operon_list) > 0:
            for op in list(set(operon_list)):
                sys.stdout.write("\t" + op + "\t" + synonym[op])
            print
        operon_list = []
    count += 1
