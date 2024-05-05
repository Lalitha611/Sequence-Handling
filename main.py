from utils import FastqProcessor
import os

accession_id = "7636289"
db_url = "sqlite:///sequence_data.db"

fastq_file1 = "inputs/fikt_A.1.fastq"
fastq_file2 = "inputs/fikt_A.2.fastq"
out_file = "outputs/out.fasta"

if __name__ == "__main__":
    # create database
    if os.path.isfile(os.path.basename(db_url)):
        print(f"Skipping database creation as the file already exists")
        # load database
        db = FastqProcessor(db_url=db_url)
    else:
        print(f"Creating new database from accession_id")
        # load database
        db = FastqProcessor(db_url=db_url)
        db.create_database_from_path(folder_path=accession_id)

    # filter sequences
    unique_sequences = db.filter_unique_sequences(forward_fastq_file=fastq_file1,
                                                  reverse_fastq_file=fastq_file2,
                                                  output_file=out_file)



