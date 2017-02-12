#!/usr/bin/python

from __future__ import division
import math
import sys

counts_matrix = sys.argv[1]
sequence_file = sys.argv[2]

# Open the argR counts matrix and append values of 'A', 'C', 'G' and 'T' to a dictionary
# Part I
myDict = {'a': [], 'c': [], 'g': [], 't': []}
with open(counts_matrix, 'r') as f:
    for line in f:
        line = line.strip()
        tmp = line.split('\t')
        # x = tmp[2:20]
        # print x
        for key in myDict:
            if tmp[0] == key:
                for i in range(2, 20):
                    myDict[key].append(int(tmp[i]))
# print myDict

myDict_1 = {"a": [], "t": [], "g": [], "c": []}
for key in myDict:
    if key in myDict_1:
        for value in myDict[key]:
            myDict_1[key].append(math.log10((float((value + 1) / 31.0)) / 0.25))
# print myDict_1['c']


# Create dictionary to store the final scores for binding sites

# Part II
scores_dict = {}
motif_dict = {}

# Assign window size based on position weight matrix sequence length

window_size = 18

# Open and assign scores to sequence file

with open(sequence_file, 'r') as f:
    for lines in f:
        # Adding gene IDs
        lines = lines.strip()
        lines = lines.split()
        scores_dict[lines[0]] = []
        motif_dict[lines[0]] = []

        # Computing binding sites using position weight matrix
        tmp = []

        for i in range(len(lines[2]) - window_size + 1):
            # Sliding window
            for j in range(i, i + window_size):
                tmp.append(lines[2][j])
            scores = 0
            # Compute score for subsequence
            for k in range(len(tmp)):
                if tmp[k] in myDict_1:
                    scores += float(myDict_1[tmp[k]][k])
            # Calculate and store scores for each 'window size' sequence in file
            scores_dict[lines[0]].append(str("".join(tmp)) + '\t' + str(scores))
            # Empty the list to re-iterate over the next set of sequence
            tmp = []

# Find scores for binding sites

for key in scores_dict:
    top_score = []
    for seq_score in scores_dict[key]:
        top_score.append(float(seq_score[19:]))
    for seq_score in scores_dict[key]:
        if str(max(top_score)) in seq_score:
            motif_dict[key].append(seq_score)

# Top 30 scores and corresponding binding sites
# Part III
all = []

for key in motif_dict:
    all.append(float(motif_dict[key][0][19:]))

top30 = []

for scores in all:
    top30.append(scores)
    if len(top30) == 31:
        top30.remove(min(top30))

for key in motif_dict:
    for seq_score in motif_dict[key]:
        for score in top30:
            if str(score) in seq_score:
                print(key + '\t' + seq_score)
