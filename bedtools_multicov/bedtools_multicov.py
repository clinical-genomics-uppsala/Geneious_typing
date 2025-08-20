#!/usr/bin/env python3

import sys
import os
import subprocess
import datetime

start_time = datetime.datetime.now()

# Path to access bundled database file in Geneious
plugin_path = os.path.dirname(__file__)

# Geneious input/output
infile = os.path.join("/geneious", sys.argv[2]).replace("\\", "/")
outfile = os.path.join("/geneious", sys.argv[4]).replace("\\", "/")

# Path to temporary Geneious folder
# Example: /Users/user/Geneious 2022.1 Data/transient/1660719270002/x/8/
path_to_geneious_data = sys.argv[6].strip()
mount_path = os.path.join(path_to_geneious_data, ":/geneious").replace("\\", "/")

# Other options
path_to_docker = sys.argv[8].strip()
bedtools_image = sys.argv[10].strip()

bedfile = sys.argv[12].strip()
bedfile_path = os.path.join(plugin_path, ":/bedfiles").replace("\\", "/")


def run_subprocess(command, name):
    """Run subprocess command, print stdout, stderr, process name and exit status"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, error) = p.communicate()
    p_status = p.wait()
    print(output.decode())
    print(f"{name} exit status: {p_status} \n")
    return output, p_status


# bedtools multicov -bams *.bam -bed  /path/to/restox_primers.bed > amplicon_counts.tsv
bedtools_multicov = (
    "bedtools multicov -bams "
    + str(os.path.join("/geneious", infile))
    + " -bed "  
    + str(os.path.join("/bedfiles", bedfile))
    + "  > /geneious/counts.tsv"
)

bedtools_subprocess = [
    path_to_docker,
    "run",
    "--rm",
    "-v",
    mount_path,
    "-v",
    bedfile_path,
    bedtools_image,
    "/bin/bash",
    "-c",
    bedtools_multicov,
]

run_subprocess(bedtools_subprocess, "bedtools_multicov")

stop_time = datetime.datetime.now()
print(
    f"bedtools completed {stop_time.strftime('%Y-%m-%d %H:%M:%S')} taking {stop_time - start_time}"
)
