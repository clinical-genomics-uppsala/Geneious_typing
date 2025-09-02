# Geneious workflow for typing of MRSA

[Geneious](https://www.geneious.com) workflow to analyze nanopore amplicon data for spa-typing and multilocus sequence typing of methicillin-resistant *Staphylococcus aureus*. 
This workflow is adapted to analyze a gene panel including *spa*, *nuc*, *lukS-lukF*, *mecA*, *mecC*, *tst* and MLST genes. 

Main steps:
- input: FASTQ files
- quality filtering with BBDuk
- sequentially mapping reads with minimap2 to spa, MLST and virulence and resistance genes respectively, continuing with unused reads to the next mapping step
- Geneious assembler to cluster spa reads [(inspired by these settings)](https://www.geneious.com/tutorials/metagenomic-analysis) and spa typing with [spatyper](https://bitbucket.org/genomicepidemiology/spatyper)
- [Krokus](https://github.com/andrewjpage/krocus) to predict sequence types (ST) from a subset of mapped MLST reads
- Counts of mapped resistance and toxin genes with bedtools multicov
- Output structure in Geneious:
````
FASTQ input files
	1_minimap_spa
	2_spa_de_novo
	3_input_spatyper
	4_spatyper
	5_minimap_mlst
	6_mlst_reads_for_krocus
	7_krokus
	8_minimap_restox
	9_restox
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

## Setup Geneious wrapper plugins

### Software versions

| Geneious_typing | image | software version |
| -------- | ------- | ------- |
| v.0.2.0 | build from spatyper/spatyper.Dockerfile | spaTyper 1.0.0 |
| v.0.2.0 | quay.io/biocontainers/krocus:1.0.3--pyhdfd78af_0 | krocus 1.0.3 |
| develop | hydragenetics/common:3.1.1.1 | bedtools v2.31.1 | 

### 1. Create spatyper wrapper plugin
Go to 'File' --> 'Create/Edit Wrapper Plugin..'. Press '+New'
- Step 1: 
	- Fill in 'Plugin Name:' and 'Menu/Button Text:' of your choice. 
	- 'Plugin Type:' select 'General Operation'. 
	- 'Bundled Program Files (optional)' add:  
		`spatyper/spatyper.py` under 'Linux' and 'Mac OSX'  
		`spatyper/spatyper.bat` under 'Windows'  
	- 'Additional Bundled Files (optional)' add:
	 `spatyper/spatyper.py` and `spatyper_db` - download [here](https://bitbucket.org/genomicepidemiology/spatyper_db/src/main/).
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
	- 'Command Line Switch': bedtools_image, 'Option Label': bedtools Docker image
	- 'Command Line Switch': bedfile, 'Option Label': name of bedfile (same name as in step 1)

<!--  -->
## Setup Geneious workflows
1. Import the reference sequences from `geneious/Saureus_references.geneious`
2. Import the workflow from `geneious/MRSA_panel.geneiousWorkflow`
3. Edit the 'Align/Assemble -> Map to Reference' steps to use the imported reference sequences (order: spa_gene, mlst_genes and restox_genes).
4. Add the spatyper, krocus and bedtools_multicov plugins to their respective steps in the workflow

## Acknowledgements

Thanks to Rene Kaden and Max Koivistoinen Jonsson for inital work and providing the reference sequence.

Comparing whole-genome sequencing with Sanger sequencing for spa typing of methicillin-resistant *Staphylococcus aureus*. Bartels MD, Petersen A, Worning P, Nielsen JB, Larner-Svensson H, Johansen HK, Andersen LP, Jarløv JO, Boye K, Larsen AR, Westh H. J. Clin. Microbiol. 2014. 52(12): 4305-8. https://pubmed.ncbi.nlm.nih.gov/25297335/

Typing of methicillin-resistant *Staphylococcus aureus* in a university hospital setting using a novel software for spa-repeat determination and database management. Harmsen D., Claus H., Witte W., Rothgänger J., Claus H., Turnwald D., & Vogel U. J. Clin. Microbiol. 2003. 41: 5442-5448. https://pubmed.ncbi.nlm.nih.gov/14662923/

The spa typing website (http://www.spaserver.ridom.de/) that is developed by Ridom GmbH and curated by SeqNet.org (http://www.SeqNet.org/).

Andrew J. Page, Jacqueline A. Keane. (2018) Rapid multi-locus sequence typing direct from uncorrected long reads using Krocus. PeerJ 6:e5233 https://doi.org/10.7717/peerj.5233

Keith A. Jolley, James E. Bray, Martin C. J. Maiden. (2018) Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications. Wellcome Open Research. 3:124 https://doi.org/10.12688/wellcomeopenres.14826.1