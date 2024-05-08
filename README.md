# Sequence Handler
This repo creates a package named sequence handler which loads in a folder containing fastq files and creates a database from this data.

# Table of Contents

- [Setup](#Setup)
- 
- [Installation](#installation)
  - [Download Files](#download-files)
  - [Database](#database)
    - [Folder Structure](#folder-structure)
  - [Misc: Formatting](#misc-formatting)



## Setup
### Download files
Sample files are downloaded from Zenodo using accession id 7636289
(https://zenodo.org/records/7636289)

|__Inputs
|   |__ 
|   |__ File2.csv
|   
|__ Output
    |__ Result1.txt
    |__ Result2.csv


Input files:
eipl_A.1.fastq
eipl_A.2.fastq
eipl_C.1.fastq
eipl_C.2.fastq

Test files:
fikt_A.1.fastq.gz
fikt_A.2.fastq.gz

Output:
out.fasta

### Installation
Before installing the required packages, install poetry. You can install it from here.
To install all the packages, run the following command from root folder.
```commandline
poetry install
```

## Run
To run the script, use
```commandline
poetry run python sequence_handler/main.py
```
The folder creates a sqlalchemy database in the given path. This database has three columns: `file path`, `sequence` and `sequence id`
This also filters out the unique sequences in the given files and writes them to output fasta file. 

### Folder structure

## Miscellaneous 
### Formatting
Formatting (lint, isort, black, mypy) can handled by running  
```
poetry run tox ""
```