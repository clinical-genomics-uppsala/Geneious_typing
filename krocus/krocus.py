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
krocus_image = sys.argv[10].strip()

database = sys.argv[12].strip()
database_path = os.path.join(plugin_path, ":/database").replace("\\", "/")

def run_subprocess(command, name):
    """Run subprocess command, print stdout, stderr, process name and exit status"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, error) = p.communicate()
    p_status = p.wait()
    print(output.decode())
    print(f"{name} exit status: {p_status} \n")
    return output, p_status


# krocus command
# krocus krocus /database/Staphylococcus_aureus_2025-06-11 /geneious/input.fastq --output_file /geneious/krocus
krocus = (
    "krocus "
    + str(os.path.join("/database", database).replace("\\", "/"))
    + " "
    + str(os.path.join("/geneious", infile).replace("\\", "/"))
    + " --output_file /geneious/krocus"
)

# Example subprocess input:
# ['/usr/local/bin/docker', 'run', '--rm', '-v', '/Users/user/Geneious 2025.1 Data/transient/1750252290559/x/941/:/geneious', \
# '-v', '/Users/user9/Geneious 2025.1 Data/WrapperPluginDevelopment/krocus/Staphylococcus_aureus_2025-06-11/:/database', \
# 'quay.io/biocontainers/krocus:1.0.1--py_0', '/bin/bash', '-c', 'krocus /database/Staphylococcus_aureus_2025-06-11 /geneious/input.fastq --output_file /geneious/krocus']
krocus_subprocess = [
    path_to_docker,
    "run",
    "--rm",
    "-v",
    mount_path,
    "-v",
    database_path,
    krocus_image,
    "/bin/bash",
    "-c",
    krocus,
]

run_subprocess(krocus_subprocess, "krocus")

stop_time = datetime.datetime.now()
print(
    f"krocus completed {stop_time.strftime('%Y-%m-%d %H:%M:%S')} taking {stop_time - start_time}"
)
