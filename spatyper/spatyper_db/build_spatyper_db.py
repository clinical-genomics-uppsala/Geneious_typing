#!/usr/bin/env python3

import argparse
import os
import csv
from Bio import SeqIO

parser = argparse.ArgumentParser(description="Build database for spatyper")
parser.add_argument("-d", "--db_folder", required=True, type=str, help="Path to database folder. Must contain spa_repeats.fna and spa_types.txt")
args = parser.parse_args()

SPA_REPEATS = os.path.join(args.db_folder, "spa_repeats.fna")
SPA_TYPES = os.path.join(args.db_folder, "spa_types.txt")
SPA_TAB = os.path.join(args.db_folder, "spa_sequences.tab")
SPA_SEQUENCES = os.path.join(args.db_folder, "spa_sequences.fna")

# Spa types dict from ridom tsv file
spa_types = {}
with open(SPA_TYPES, "r") as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',', fieldnames=["type", "repeats"])
    spa_types = {row["type"]: row["repeats"] for row in csvreader}
print(f"Total spa types: {len(spa_types)}")

# Repeat FASTA sequences from ridom
spa_repeats = {}
for record in SeqIO.parse(SPA_REPEATS, "fasta"):
    spa_repeats[record.id]=str(record.seq)
print(f"Total spa repeats: {len(spa_repeats)}")

# For each spatype, split repeat seq and look up each in fasta file and append to new record
spa_records = {}
for spatype, repeats in spa_types.items():
    spa_sequence = ""
    repeat_nos = repeats.strip().split('-')
    for repeat_no in repeat_nos:
        repeat_name = str("r"+repeat_no.strip())
        if repeat_name in spa_repeats:
            spa_sequence += spa_repeats[repeat_name]
        else:
            print(f"Missing repeat {repeat_name} for spa type {spatype}")
            break
    spatype_fasta_name = "spatype_" + spatype
    spa_records[spatype_fasta_name] = spa_sequence
print(f"Successfully built spa sequences: {len(spa_records)}")

# Write spa sequences to fasta format
with open(SPA_TAB, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    for record in spa_records.items():
        writer.writerow(record)
SeqIO.convert(SPA_TAB, "tab", SPA_SEQUENCES, "fasta-2line")
print(f"Updated database saved at: {os.path.abspath(SPA_SEQUENCES)}")