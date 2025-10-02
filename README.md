# Geneious workflow for typing of MRSA

[Geneious](https://www.geneious.com) workflow to analyze nanopore amplicon data for spa-typing and multilocus sequence typing of methicillin-resistant *Staphylococcus aureus*. 
This workflow is adapted to analyze a gene panel including *spa*, *nuc*, *lukS-lukF*, *mecA*, *mecC*, *tst* and MLST genes. 

Main steps:
- input: FASTQ files
- quality filtering with BBDuk
- sequentially mapping reads with minimap2 to spa, MLST and virulence and resistance genes respectively, continuing with unused reads to the next mapping step
- Geneious assembler to cluster spa reads [(inspired by these settings)](https://www.geneious.com/tutorials/metagenomic-analysis), annotation of spa repeats and spa typing with [spatyper](https://bitbucket.org/genomicepidemiology/spatyper)
- [Krokus](https://github.com/andrewjpage/krocus) to predict sequence types (ST) from a subset of mapped MLST reads
- Counts of mapped resistance and toxin genes with bedtools multicov
- Excel report with results for multiple samples
- Output structure in Geneious:
````
FASTQ input files
	01_minimap_spa
	02_spa_de_novo
	03_spa_de_novo_annotated
	04_input_spatyper
	05_spatyper
	06_minimap_mlst
	07_mlst_reads_for_krocus
	08_krokus
	09_minimap_restox
	10_restox
````


## System requirements
The workflow is tested on Windows and Mac, but may work on Linux.
- Geneious
- Python 3
- Docker
- [Geneious Wrapper Plugin Creator](https://www.geneious.com/api-developers/)

&nbsp;
&nbsp;

# Installation

## Add spa repeat annotations to Geneious
1. Copy the spa repeats from [https://spa.ridom.de/repeats.shtml](https://spa.ridom.de/repeats.shtml) and save as a tsv file.
2. Create a new folder in Geneious and import the tsv file. Select 'Import Type: Primer' and column 1 as 'Name' and column 3 as 'Sequence'.
3. Select all imported documents and go to the annotations tab. Select all annotations and press 'Edit Annotations'.
Under name select 'Copy name from: Sequence property' and 'Property: Sequence Name'. Change the annotation type to 'Repeat Region'.

## Setup Geneious wrapper plugins

### Required docker images and software versions

| Geneious_typing | image | software version |
| -------- | ------- | ------- |
| v.0.3.0 | build from spatyper/spatyper.Dockerfile | spaTyper 1.0.0 |
| v.0.3.0 | quay.io/biocontainers/krocus:1.0.3--pyhdfd78af_0 | krocus 1.0.3 |
| v.0.3.0 | hydragenetics/common:3.1.1.1 | bedtools v2.31.1 | 
| v.0.3.0 | hydragenetics/common:3.1.1.1 | xlsxwriter 3.2.3 | 

### 1. Create spatyper wrapper plugin
Go to 'File' --> 'Create/Edit Wrapper Plugin..'. Press '+New'
- Step 1: 
	- Fill in 'Plugin Name:' and 'Menu/Button Text:' of your choice. 
	- 'Plugin Type:' select 'General Operation'. 
	- 'Bundled Program Files (optional)' add:  
		`spatyper/spatyper.py` under 'Linux' and 'Mac OSX'  
		`spatyper/spatyper.bat` under 'Windows'  
	- 'Additional Bundled Files (optional)' add:
	 `spatyper/spatyper.py` and `spatyper_db` - download [here](https://bitbucket.org/genomicepidemiology/spatyper_db/).
- Step 2: 
	- 'Sequence Type:' select 'Nucleotide only'.
	- 'Document Type:' select 'Single Sequence'.
	- 'Format': 'FASTA sequences/alignment'
	- 'Command Line':
		`-i [inputFileNames] -o spaType_results.tsv -g [inputFolderName] [otherOptions]`
	- Under 'Output' 'File Name:' `spaType_results.tsv` and select 'Format:' 'Text file (plain)' and 'Name in Geneious:' `[inputNames]`
	- Check 'Save 'Standard Out' as a note on the first output document'
- Step 3:  
	Press 'Add' to add two user options (in this order):
	- 'Command Line Switch': path_to_docker, 'Option Label': Path to Docker
	- 'Command Line Switch': spatyper_image, 'Option Label': Spatyper Docker image
 
	Both 'Command Line Switch' and 'Option Label' should be filled in. Labels can be customized.

### 2. Create krocus wrapper plugin
Go to 'File' --> 'Create/Edit Wrapper Plugin..'. Press '+New'
- Step 1: 
	- Fill in 'Plugin Name:' and 'Menu/Button Text:' of your choice. 
	- 'Plugin Type:' select 'General Operation'. 
	- 'Bundled Program Files (optional)' add:  
		`krocus/krocus.py` under 'Linux' and 'Mac OSX'  
		`krocus/krocus.bat` under 'Windows'  
	- 'Additional Bundled Files (optional)' add:
	 `krocus/krocus.py` and a folder with the [PubMLST database](https://pubmlst.org) for *S*.*aureus*.
- Step 2: 
	- 'Sequence Type:' select 'Nucleotide only'.
	- 'Document Type:' select 'Unaligned Sequences (1+)'.
	- 'Format': 'FastQ (Sanger scores)'
	- 'Command Line':
		`-i [inputFileNames] -o krocus -g [inputFolderName] [otherOptions]`
	- Under 'Output' 'File Name:' `krocus` and select 'Format:' 'Text file (plain)' and 'Name in Geneious:' `[inputNames]`
	- Check 'Save 'Standard Out' as a note on the first output document'
- Step 3:  
	Press 'Add' to add two user options (in this order):
	- 'Command Line Switch': path_to_docker, 'Option Label': Path to Docker
	- 'Command Line Switch': krocus_image, 'Option Label': Krocus Docker image
	- 'Command Line Switch': database, 'Option Label': Path to MLST database (same folder name as in step 1)

### 3. Create bedtools_multicov wrapper plugin
Go to 'File' --> 'Create/Edit Wrapper Plugin..'. Press '+New'
- Step 1: 
	- Fill in 'Plugin Name:' and 'Menu/Button Text:' of your choice. 
	- 'Plugin Type:' select 'General Operation'. 
	- 'Bundled Program Files (optional)' add:  
		`bedtools_multicov/bedtools_multicov.py` under 'Linux' and 'Mac OSX'  
		`bedtools_multicov/bedtools_multicov.bat` under 'Windows'  
	- 'Additional Bundled Files (optional)' add:
	 `bedtools_multicov/bedtools_multicov.py` and the bedfile for the resistance and toxin genes `bedtools_multicov/restox_primers.bed`.
- Step 2: 
	- 'Sequence Type:' select 'Nucleotide only'.
	- 'Document Type:' select 'Multiple alignment (3+ sequences)'.
	- 'Format': 'BAM sequences/alignments'. Press 'Input Format Options..' and check the 'Export BAM index file' box.
	- 'Command Line':
		`-i [inputFileNames] -o counts.tsv -g [inputFolderName] [otherOptions]`
	- Under 'Output' 'File Name:' `counts.tsv` and select 'Format:' 'Text file (plain)' and 'Name in Geneious:' `[inputNames]`
	- Check 'Save 'Standard Out' as a note on the first output document'
- Step 3:  
	Press 'Add' to add two user options (in this order):
	- 'Command Line Switch': path_to_docker, 'Option Label': Path to Docker
	- 'Command Line Switch': bedtools_image, 'Option Label': bedtools Docker image (hydragenetics/common)
	- 'Command Line Switch': bedfile, 'Option Label': name of bedfile (same name as in step 1)

### 4. Create MRSA_report wrapper plugin
Go to 'File' --> 'Create/Edit Wrapper Plugin..'. Press '+New'
- Step 1: 
	- Fill in 'Plugin Name:' and 'Menu/Button Text:' of your choice. 
	- 'Plugin Type:' select 'General Operation'. 
	- 'Bundled Program Files (optional)' add:  
		`report/run_report.py` under 'Linux' and 'Mac OSX'  
		`report/run_report.bat` under 'Windows'  
	- 'Additional Bundled Files (optional)' add:
	 `report/run_report.py` and `report/MRSA_report.py`.
- Step 2: 
	- 'Sequence Type:' select 'Nucleotide only'.
	- 'Document Type:' select 'Unaligned sequences (1+)'.
	- 'Format': 'FastQ Compressed (Sanger scores)'.
	- 'Command Line':
		`[otherOptions] 2>&1 > log.txt`
	- Under 'Output' 'File Name:' `log.txt` and select 'Format:' 'Text file (plain)' and 'Name in Geneious:' `log`
	- Check 'Save 'Standard Out' as a note on the first output document'
- Step 3:  
	Press 'Add' to add two user options (in this order):
	- 'Command Line Switch': path_to_docker, 'Option Label': Path to Docker
	- 'Command Line Switch': report_image, 'Option Label': report Docker image (hydragenetics/common)
	- 'Command Line Switch': path_to_data, 'Option Label': Data path

## Setup Geneious workflow
1. Import the reference sequences from `geneious/Saureus_references.geneious`
2. Import the workflow from `geneious/MRSA_panel.geneiousWorkflow`
3. Edit the 'Align/Assemble -> Map to Reference' steps to use the imported reference sequences (order: spa_gene, mlst_genes and restox_genes)
4. Add folder with spa repeat annotations to step 'Annotate from Database'
5. Add the spatyper, krocus, bedtools_multicov and MRSA_report plugins to their respective steps in the workflow
6. Edit the path to the three export steps (must be the same as path_to_data in the MRSA_report plugin)

## Acknowledgements

Thanks to Rene Kaden and Max Koivistoinen Jonsson for inital work and providing the reference sequence.

Comparing whole-genome sequencing with Sanger sequencing for spa typing of methicillin-resistant *Staphylococcus aureus*. Bartels MD, Petersen A, Worning P, Nielsen JB, Larner-Svensson H, Johansen HK, Andersen LP, Jarløv JO, Boye K, Larsen AR, Westh H. J. Clin. Microbiol. 2014. 52(12): 4305-8. https://pubmed.ncbi.nlm.nih.gov/25297335/

Typing of methicillin-resistant *Staphylococcus aureus* in a university hospital setting using a novel software for spa-repeat determination and database management. Harmsen D., Claus H., Witte W., Rothgänger J., Claus H., Turnwald D., & Vogel U. J. Clin. Microbiol. 2003. 41: 5442-5448. https://pubmed.ncbi.nlm.nih.gov/14662923/

The spa typing website (http://www.spaserver.ridom.de/) that is developed by Ridom GmbH and curated by SeqNet.org (http://www.SeqNet.org/).

Andrew J. Page, Jacqueline A. Keane. (2018) Rapid multi-locus sequence typing direct from uncorrected long reads using Krocus. PeerJ 6:e5233 https://doi.org/10.7717/peerj.5233

Keith A. Jolley, James E. Bray, Martin C. J. Maiden. (2018) Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications. Wellcome Open Research. 3:124 https://doi.org/10.12688/wellcomeopenres.14826.1