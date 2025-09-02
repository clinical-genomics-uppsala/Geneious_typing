#!/usr/bin/env python3

import sys
import os
import csv
import re
import datetime
import xlsxwriter

##### Constants #####
FOLDER = sys.argv[1]
SPA_FILE_PATTERN = "_spa.txt$"
KROCUS_FILE_PATTERN = "_\S{1,5}_sequences.txt$"
RESTOX_FILE_PATTERN = "_restox.txt$"
SPA_FIELDS = ["#spa Type", "Repeats"]
KROCUS_FIELDS = ["sequence type", "coverage", "yqiL", "gmk", "aroE", "pta", "arcC", "tpi", "glpF"]
RESTOX_FIELDS = ['reference','pos1','pos2','gene','count']
REPORT_HEADER = ["sample"] + SPA_FIELDS + KROCUS_FIELDS + ["nuc", "pvl", "mecA", "mecC", "tst", "date"]
EXCEL_FILE = os.path.join(FOLDER,"MRSA_results.xlsx")
WORKSHEET_NAME = "MRSA_panel_results"

##### Functions for parsing input data #####
def create_sample_dict(folder, ending):
    """Create dict with sample names and file paths"""
    sample_dict = {}
    for file in os.listdir(folder):
        if re.search(ending, file):
            sample_dict[re.split(ending, file)[0].strip()] = (
                os.path.join(folder, file)
            )
    sample_dict = dict(sorted(sample_dict.items()))  # sort by sample name
    return sample_dict

def read_spa_txt(sample_dict, fields):
    """
        Read spa txt file and get spa type and repeats
        File with two-line header
        Return a nested dict with sample names and spa results
    """
    results = {}
    for sample, file in sample_dict.items():
        with open(file, 'r') as csvfile:
            next(csvfile)
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for row in csvreader:
                spa_data = {gene: row[gene] for gene in fields}
                results[sample] = {
                    **spa_data
                }
                break
    return results

def read_restox_txt(sample_dict, fields):
    """
        Read restox txt file and get no of mapped reads per gene
        File with no header
        Return a nested dict with sample names and read counts per gene
    """
    results = {}
    for sample, file in sample_dict.items():
        results[sample] = {}
        with open(file, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t', fieldnames=fields)
            for row in csvreader:
                gene = row['gene']
                count = row['count']
                results[sample][gene] = int(count)
    return results

def read_krocus_txt(sample_dict, fields):
    """
        Read krocus txt file and get ST and alleles for the best coverage row
        File with no header
        Get row with highest coverage
        Return a nested dict with sample names, ST, coverage and alleles
        When no allele is found add NA to dict
    """
    results = {}
    for sample, file in sample_dict.items():
        with open(file, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter='\t', fieldnames=fields, restval="NA")
                sorted_rows = sorted(csvreader, key=lambda d: float(d['coverage']), reverse=True)
                for s, row in enumerate(sorted_rows, start=1):
                    if s == 1:
                        krocus_data = {gene: row[gene] for gene in fields[0:2]}

                        # Initialize all allele values with 'NA'
                        for gene in fields[2:]:
                            krocus_data[gene] = "NA"

                        # Try to match each value to a fieldname
                        for value in row.values():
                            match = re.match("(^\S+)\(", str(value).lower())
                            if match:
                                gene_name = match.group(1)
                                for gene in fields[2:]:
                                    if gene.lower() == gene_name and krocus_data[gene] == "NA":
                                        krocus_data[gene] = value
                                        break

                        results[sample] = krocus_data
    return results

def combine_results(dict_list):
    """ Concatenate dicts with same keys """
    concat_dict = {}
    for d in dict_list:
        for sample, data in d.items():
            if sample not in concat_dict:
                concat_dict[sample] = {}
            concat_dict[sample].update(data)
    return concat_dict


##### Functions for writing to excel #####
def report_header_to_dict (header):
    """ Adapt header list to format required by Excel data table """
    header_list = []
    for name in header:
        header_dict = {}
        header_dict['header'] = name
        header_list.append(header_dict)
    return header_list

def convert_colno_to_letter(colno):
    """ Convert column number to Excel column letter (works for <27 columns)"""
    letter = chr(colno + 64)
    return letter

def write_nested_dict_to_table(nested_dict, worksheet, header, fill_value):
    """ Write table contents
        Each row starts with outer keys, followed by the values
        Fill missing data with fill_value
        Skip first row = header
    """
    for row, sample in enumerate(sorted(nested_dict.keys()), start=1):
        worksheet.write(row, 0, sample)
        for col, field in enumerate(header[1:], start=1):
            value = nested_dict[sample].get(field, fill_value)
            worksheet.write(row, col, value)

def fill_last_column(worksheet, dictionary, header, text):
    """ Fill last column with "text" """
    new_col = [text]*len(dictionary)
    worksheet.write_column(1, len(header)-1, new_col)


##### Read and concatenate data  #####
spa_samples = create_sample_dict(FOLDER, SPA_FILE_PATTERN)
spa_results = read_spa_txt(spa_samples, SPA_FIELDS)

krocus_samples = create_sample_dict(FOLDER, KROCUS_FILE_PATTERN)
krocus_results = read_krocus_txt(krocus_samples, KROCUS_FIELDS)

restox_samples = create_sample_dict(FOLDER, RESTOX_FILE_PATTERN)
restox_results = read_restox_txt(restox_samples, RESTOX_FIELDS)

all_results = combine_results([spa_results, krocus_results, restox_results])


##### Write to excel  #####
workbook = xlsxwriter.Workbook(EXCEL_FILE)
workbook.formats[0].set_font_size(14)

worksheet_results = workbook.add_worksheet(WORKSHEET_NAME)

report_header_list = report_header_to_dict(REPORT_HEADER)
table_area = "A1:" + convert_colno_to_letter(len(REPORT_HEADER)) + str(len(all_results)+1)
worksheet_results.add_table(table_area, {'columns': report_header_list,'banded_rows': True,'first_column': True, 'style': 'Table Style Light 2'})

write_nested_dict_to_table(all_results, worksheet_results, REPORT_HEADER, "no data")

fill_last_column(worksheet_results, all_results, REPORT_HEADER, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

worksheet_results.autofit()

workbook.close()