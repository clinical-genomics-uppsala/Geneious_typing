# Updating the spatyper database

Dependencies: [biopython](https://biopython.org/)

1. Create a new directory, for example `spatyper_db_YYYY-MM-DD`
2. Go to the spa typing website (http://www.spaserver.ridom.de/) and download spa types `spa_types.txt` and the spa repeat sequences `spa_sequences.fna` 
3. Run `python build_spatyper_db.py --db_folder <path to spatyper_db_YYYY-MM-DD>`