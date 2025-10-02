:: Path to current directory to bundled optional files
set plugin_path=%~dp0

:: Output to Geneious
set infile=%2
set outfile=%4

:: Options from Geneious
set path_to_geneious_data=%6
shift
shift
shift
shift
set path_to_docker=%4
set bedtools_image=%6
set bedfile=%8

python "%plugin_path%bedtools_multicov.py" -i %infile% -o %outfile% -g %path_to_geneious_data% -d %path_to_docker% -k %bedtools_image% -b %bedfile%

:: Wrapper Plugin Creator command line: -i [inputFileNames] -o counts.tsv -g [inputFolderName] [otherOptions]
:: path_to_docker bedtools_image bedfile