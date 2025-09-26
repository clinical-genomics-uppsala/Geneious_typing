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
set spatyper_image=%6
set database=%8

python "%plugin_path%spatyper.py" -i %infile% -o %outfile% -g %path_to_geneious_data% -d %path_to_docker% -k %spatyper_image% -b %database%

:: Wrapper Plugin Creator command line: -i [inputFileNames] -o spaType_results.tsv -g [inputFolderName] [otherOptions]
:: path_to_docker spatyper_image database