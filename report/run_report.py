#!/usr/bin/env python3

import sys
import os
import subprocess
import datetime

start_time = datetime.datetime.now()

# Path to access bundled database file in Geneious
plugin_path = os.path.dirname(__file__)

# Other options
path_to_docker = sys.argv[2].strip()
report_image = sys.argv[4].strip()

# In/out data folder selected by user
path_to_data = sys.argv[6]
mount_path = os.path.join(path_to_data, ":/user_data")


def run_subprocess(command, name):
    """Run subprocess command, print stdout, stderr, process name and exit status"""
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output, error) = p.communicate()
    p_status = p.wait()
    print(output.decode())
    print(f"{name} exit status: {p_status} \n")
    return output, p_status


# Generate Excel report
run_report = (
    "python /scripts/MRSA_report.py  /user_data"
)

report_subprocess = [
    path_to_docker,
    "run",
    "--rm",
    "-v",
    os.path.join(plugin_path, ":/scripts"),
    "-v",
    mount_path,
    report_image,
    "/bin/bash",
    "-c",
    run_report,
]

run_subprocess(report_subprocess, "report")

# Write to log file
stop_time = datetime.datetime.now()
print(
    f"""
    Report completed {stop_time.strftime('%Y-%m-%d %H:%M:%S')} taking {stop_time - start_time}
    Report saved at {path_to_data}
    """
)