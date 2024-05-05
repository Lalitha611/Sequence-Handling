from utils import FastqProcessor, load_database_as_dataframe
import os

accession_id = "7636289"
db_url = "sqlite:///sequence_data.db"


if __name__ == "__main__":
    # create database
    if os.path.isfile(os.path.basename(db_url)):
        print(f"Skipping database creation as the file already exists")
    else:
        print(f"Creating new database from accession_id")
        db = FastqProcessor(db_url=db_url)
        db.create_database_from_path(folder_path=accession_id)

    # load database
    df = load_database_as_dataframe(db_url=db_url)
    print(df.head())

