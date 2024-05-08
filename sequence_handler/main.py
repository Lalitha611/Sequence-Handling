import os
import argparse

from sequence_handler.utils.data_utils import create_database_from_path, \
    load_database_as_dataframe, \
    filter_unique_sequences


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process FASTQ files and generate output file')
    parser.add_argument('--accession_id',
                        type=str,
                        required=True,
                        help='Accession ID for the sequence data')
    parser.add_argument('--db_url',
                        type=str,
                        default="sqlite:///sequence_data.db",
                        help='Database URL for storing sequence data')
    parser.add_argument('--fastq_file1',
                        type=str,
                        required=True,
                        help='Path to the forward FASTQ file')
    parser.add_argument('--fastq_file2',
                        type=str,
                        required=True,
                        help='Path to the reverse FASTQ file')
    parser.add_argument('--out_file',
                        type=str,
                        required=True,
                        help='Path to the output fastq file')

    args = parser.parse_args()

    # create database
    if os.path.isfile(os.path.basename(args.db_url)):
        print(f"Skipping database creation as the file already exists")
    else:
        print(f"Creating new database from accession_id")
        create_database_from_path(db_url=args.db_url, folder_path=args.accession_id)

    # filter sequences
    unique_sequences = filter_unique_sequences(db_url=args.db_url,
                                               forward_fastq_file=args.fastq_file1,
                                               reverse_fastq_file=args.fastq_file2,
                                               output_file=args.out_file)


    # load database as pandas dataframe
    df = load_database_as_dataframe(args.db_url)
    df.head()
