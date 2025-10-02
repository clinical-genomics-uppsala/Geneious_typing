:: Path to current directory to bundled optional files
set plugin_path=%~dp0

:: Options from Geneious
set path_to_docker=%2
set report_image=%4
set path_to_data=%6


python "%plugin_path%run_report.py" -d %path_to_docker% -r %report_image% -f %path_to_data%

:: Wrapper Plugin Creator command line: [otherOptions] 2>&1 > log.txt
