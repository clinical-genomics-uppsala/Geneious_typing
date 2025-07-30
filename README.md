# Geneious workflow for typing of MRSA

[Geneious](https://www.geneious.com) workflow to analyze nanopore amplicon data for spa-typing and multilocus sequence typing of methicillin-resistant *Staphylococcus aureus*.

This workflow is adapted to analyze a gene panel including *spa*, *nuc*, *lukS-lukF*, *mecA*, *mecC*, *tst* and MLST genes.  
This is a draft workflow including filtering av mapping of reads to an artificial reference sequence.

## Setup Geneious workflows
1. Import the reference sequence from `geneious/TestRefSeq_V.2.geneious`
2. Import the workflow from `geneious/MRSA_panel_2024-04-25.geneiousWorkflow`
3. Edit the 'Align/Assemble' step to use the imported reference sequence.

## Acknowledgements

Thanks to Rene Kaden and Max Koivistoinen Jonsson for inital work and providing the reference sequence.