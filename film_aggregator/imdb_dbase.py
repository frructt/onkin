
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Column,Integer,String
import glob
import os
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from film_aggregator.models import ImdbBasicName
from film_aggregator import db


# Define structure of table
class ImdbBasicNameDTO(object):
    def __init__(self, nconst, primary_name, birth_year, death_year, primary_profession, known_for_titles):
        self.nconst = nconst
        self.primary_name = primary_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.primary_profession = primary_profession
        self.known_for_titles = known_for_titles

    def __repr__(self):
        return f'{self.nconst, self.primary_name, self.birth_year, self.death_year, self.primary_profession, self.known_for_titles}'


def create_table(folder_of_files):
    # Get list of files in folder
    files = glob.glob(os.path.join(folder_of_files, "name.basics.tsv"))

    # Loop through all files in list
    for file_name in files:

        # Read file into dataframe
        headers = ["primaryId",	"primaryName",	"birthYear",	"deathYear",	"primaryProfession", "knownForTitles"]
        df = pd.read_csv(file_name, error_bad_lines=False, nrows=100000, header=None, names=headers,
                         skiprows=1, sep='\t+', engine='python', na_values=['\\N'])
        df = df.where(pd.notnull(df), None)

        # solution #1
        df = pd.DataFrame(data=df)
        df.to_sql('ImdbBasicName', con=db.engine, index_label=None, if_exists="append")

        # solution #2
        # Convert dataframe to list and store in same variable
        # df = df.values.tolist()
        # Loop through list of lists, each list in create_bom_table.xls_data is a row
        # for row in df:
        #     # Each element in the list is an attribute for the table class
        #     # Iterating through rows and inserting into table
        #     imdb_basic_name = ImdbBasicName(nconst=row[0], primary_name=row[1], birth_year=row[2], death_year=row[3],
        #                                     primary_profession=row[4], known_for_titles=row[5])
        #     existed_basic_name = ImdbBasicName.query.filter_by(nconst=imdb_basic_name.nconst).first()
        #     if not existed_basic_name:
        #         db.session.add(imdb_basic_name)
        #         db.session.commit()
