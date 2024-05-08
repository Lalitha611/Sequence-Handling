from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class DatabaseManager:
    """
    Class for managing sqlalchemy database
    """
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


class FastqSequence(Base):
    """
    class for fastqsequence format in database
    """
    __tablename__ = "fastq_sequences"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String)
    sequence_id = Column(Text)
    sequence = Column(Text)
