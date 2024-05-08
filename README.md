# Sequence Handler
This repo creates a package named sequence handler which loads in a folder containing fastq files and creates a database from this data.

# Table of Contents

- [Setup](#Setup)
- [Installation](#installation)
  - [Download Files](#download-files)
  - [Misc: Formatting](#Formatting)



## Setup
### Download files
Sample files are downloaded from Zenodo using accession id 7636289
(https://zenodo.org/records/7636289)

```
project
   README.md    
│
└───7636289:
│   │   eipl_A.1.fastq
│   │   │  eipl_A.1.fastq
│   │   eipl_A.2.fastq
│   │   │  eipl_A.2.fastq
│   │   eipl_C.1.fastq
│   │    │  eipl_C.1.fastq
│   │   eipl_C.2.fastq
│   │    │  eipl_C.2.fastq
│   │
└───Inputs:
│   |  fikt_A.1.fastq
│   |  fikt_A.2.fastq
|
└───Outputs:
|    |  out.fasta
```

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

## Miscellaneous 
### Formatting
Formatting (lint, isort, black, mypy) can handled by running  
```
poetry run tox ""
```
