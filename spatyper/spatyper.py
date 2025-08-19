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
spatyper_image = sys.argv[10].strip()

database_path = os.path.join(plugin_path, ":/database").replace("\\", "/")


def run_subprocess(command, name):
    """Run subprocess command, print stdout, stderr, process name and exit status"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, error) = p.communicate()
    p_status = p.wait()
    print(output.decode())
    print(f"{name} exit status: {p_status} \n")
    return output, p_status


# spatyper command:
# python3 spatyper/spatyper.py -i /geneious/input.fasta -db /database/spatyper_db/ -o /geneious
spatyper = (
    "python3 spatyper/spatyper.py -i "
    + str(os.path.join("/geneious", infile))
    + " -db /database/spatyper_db/ -o /geneious"
)

# Example subprocess input:
# ['/usr/local/bin/docker', 'run', '--rm', '-v', '/Users/user/Geneious 2025.1 Data/transient/1750252290559/x/950/:/geneious', \
# '-v', '/Users/user/Geneious 2025.1 Data/WrapperPluginDevelopment/spatyper/:/database', 'spatyper:2025-02-12', \
# '/bin/bash', '-c', 'python3 spatyper/spatyper.py -i /geneious/input.fasta -db /database/spatyper_db/ -o /geneious']
spatyper_subprocess = [
    path_to_docker,
    "run",
    "--rm",
    "-v",
    mount_path,
    "-v",
    database_path,
    spatyper_image,
    "/bin/bash",
    "-c",
    spatyper,
]

run_subprocess(spatyper_subprocess, "spatyper")

stop_time = datetime.datetime.now()
print(
    f"spatyper completed {stop_time.strftime('%Y-%m-%d %H:%M:%S')} taking {stop_time - start_time}"
)
