import logging
import os
from dataclasses import dataclass
from tqdm import tqdm
import pandas as pd
from Bio import SeqIO
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger


def get_fastq_files(folder_path):
    fastq_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".fastq"):
                fastq_files.append(os.path.join(root, file))
    return fastq_files


def create_dataframe_from_path(folder_path):
    fastq_files = get_fastq_files(folder_path)
    data = []
    for each in fastq_files:
        for record in SeqIO.parse(each, "fastq"):
            sequence = str(record.seq)
            data.append([each, sequence])

    df = pd.DataFrame(data, columns=["File path", "Sequence"])
    return df


@dataclass
class FastqProcessor:
    Base = declarative_base()

    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def create_database_from_path(self, folder_path, table_name="fastq_sequences"):
        session = self.Session()

        class FastqSequence(self.Base):
            __tablename__ = table_name
            id = Column(Integer, primary_key=True, autoincrement=True)
            file_path = Column(String)
            sequence = Column(Text)

        fastq_files = get_fastq_files(folder_path)
        for i, each in tqdm(enumerate(fastq_files), total=len(fastq_files), desc= "Writing files to database"):
            for record in SeqIO.parse(each, "fastq"):
                sequence = str(record.seq)
                fastq_sequence = FastqSequence(file_path=each, sequence=sequence)
                session.add(fastq_sequence)
        session.commit()
        session.close()


def load_database_as_dataframe(db_url, table_name="fastq_sequences"):
    engine = create_engine(db_url)
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql_table(table_name, conn)
    return df
