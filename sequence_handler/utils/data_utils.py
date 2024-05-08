from loguru import logger
import os
from tqdm import tqdm
import pandas as pd
from Bio import SeqIO
from sqlalchemy import create_engine
from sequence_handler.utils.common import DatabaseManager, FastqSequence


def get_fastq_files(folder_path: str) -> list:
    """
    Fetches the fastq files given the folder path
    Args:
        folder_path: the path of folder or accession id where fastq files are stored

    Returns:
        a list of fastq files in the folder

    """
    fastq_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".fastq"):
                fastq_files.append(os.path.join(root, file))
    return fastq_files


def create_dataframe_from_path(folder_path: str) -> pd.DataFrame:
    """
    Creates pandas dataframe from fastq files folder
    Args:
        folder_path: the path of the fastq files

    Returns:
        a pandas dataframe containing fastq data

    """
    fastq_files = get_fastq_files(folder_path)
    data = []
    for each in fastq_files:
        for record in SeqIO.parse(each, "fastq"):
            sequence = str(record.seq)
            data.append([each, sequence])

    df = pd.DataFrame(data, columns=["File path", "Sequence"])
    return df


def create_database_from_path(db_url: str, folder_path: str) -> None:
    """
    creates sqlalchemy database from folder of fastq files
    Args:
        db_url: the uri of the database where it has to be stored
        folder_path: the folder path containing fastq files

    Returns:
        None

    """
    db_manager = DatabaseManager(db_url=db_url)
    session = db_manager.Session()
    try:
        fastq_files = get_fastq_files(folder_path)
        for i, each in enumerate(tqdm(fastq_files)):
            for record in SeqIO.parse(each, "fastq"):
                sequence = str(record.seq)
                sequence_id = str(record.description)
                fastq_sequence = FastqSequence(file_path=each, sequence_id=sequence_id, sequence=sequence)
                session.add(fastq_sequence)
        session.commit()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        session.rollback()
    finally:
        session.close()


def filter_unique_sequences(db_url: str, forward_fastq_file: str, reverse_fastq_file: str,
                            output_file: str | None = None) -> dict:
    """
    Filters the unique sequences which are not present in the database
    Args:
        db_url: uri of the existing database
        forward_fastq_file: the forward fastq file
        reverse_fastq_file: the reverse fastq file
        output_file: the output path where fasta file has to be stored

    Returns:
        a dictionary with all unique sequences and descriptions
    """
    db_manager = DatabaseManager(db_url=db_url)
    session = db_manager.Session()
    try:
        unique_seqs_descs = {}
        logger.info("Filtering unique sequences")
        for seq_record1, seq_record2 in zip(SeqIO.parse(forward_fastq_file, "fastq"),
                                            SeqIO.parse(reverse_fastq_file, "fastq")):
            seq = str(seq_record1.seq)
            desc = seq_record1.description
            if seq not in unique_seqs_descs:
                unique_seqs_descs[seq] = desc

            seq = str(seq_record2.seq)
            desc = seq_record2.description
            if seq not in unique_seqs_descs:
                unique_seqs_descs[seq] = desc

        database_sequences = {seq.sequence for seq in session.query(FastqSequence).all()}
        unique_seqs_descs = {seq: desc for seq, desc in unique_seqs_descs.items() if seq not in database_sequences}

        logger.info(f"Number of unique sequences found are {len(unique_seqs_descs)}")

        if output_file:
            logger.info(f"Writing unique sequences to {output_file}")
            with open(output_file, "w") as f:
                for seq, desc in sorted(unique_seqs_descs.items()):
                    f.write(f">{desc}\n{seq}\n")

        return unique_seqs_descs
    except Exception as e:
        logger.error(f"Error filtering unique sequences: {e}")
    finally:
        session.close()


def load_database_as_dataframe(db_url: str, table_name: str = "fastq_sequences") -> pd.DataFrame:
    """
    loads a sqlalchemy database as pandas dataframe
    Args:
        db_url: the uri of the exisiting database
        table_name: name of the table saved in database

    Returns:
        a pandas dataframe containing fastq data

    """
    engine = create_engine(db_url)
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql_table(table_name, conn)
    return df
