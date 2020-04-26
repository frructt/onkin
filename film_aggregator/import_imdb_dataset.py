import glob
import os

import pandas as pd
import requests

from film_aggregator import db


name_basic_url = "https://datasets.imdbws.com/name.basics.tsv.gz"
name_basics_headers = ["primaryId", "primaryName", "birthYear", "deathYear", "primaryProfession", "knownForTitles"]
name_basics_dtypes = {"primaryId": "str", "primaryName": "str", "birthYear": "float32", "deathYear": "float32",
                      "primaryProfession": "str", "knownForTitles": "str"}

akas_url = ""
akas_headers = ["titleId", "ordering", "title", "region", "language", "types", "attributes", "isOriginalTitle"]
akas_dtypes = {"titleId": "str", "ordering": "float32", "title": "str", "region": "str", "language": "str",
               "types": "str", "attributes": "str", "isOriginalTitle": "float32"}

crew_url = ""
crew_headers = ["primaryId", "directors", "writers"]
crew_dtypes = {"primaryId": "str", "directors": "str", "writers": "str"}

episode_url = ""
episode_headers = ["primaryId", "parentPrimaryId", "seasonNumber", "episodeNumber"]
episode_dtypes = {"primaryId": "str", "parentPrimaryId": "str", "seasonNumber": "float32", "episodeNumber": "float32"}

raitings_url = ""
raitings_headers = ["primaryId", "averageRating", "numVotes"]
raitings_dtypes = {"primaryId": "str", "averageRating": "float32", "numVotes": "float32"}

title_basics_url = ""
title_basics_headers = ["primaryId", "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "endYear",
                        "runtimeMinutes", "genres"]
title_basics_dtypes = {"primaryId": "str", "titleType": "str", "primaryTitle": "str", "originalTitle": "str",
                       "isAdult": "float32", "startYear": "float32", "endYear": "float32", "runtimeMinutes": "float32",
                       "genres": "str"}


def download_file(filepath, url):
    local_filename = url.split("/")[-1].rsplit(".", 1)[0]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"{filepath}/{local_filename}", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    # f.flush()
    return f"{filepath}/{local_filename}"


def import_dataset(dataset_file, headers, dtypes, base_name):
    # Get list of files in folder
    # files = glob.glob(os.path.join(folder_of_files, "name.basics.tsv"))
    # dataset_file = download_file(filepath, name_basic_url)

    # Read file into dataframe
    # dataset_file = "{}/{}.tsv".format(filepath, "name.basic")
    df_chunk = pd.read_csv(dataset_file, chunksize=10, nrows=100, error_bad_lines=False, header=None,
                           names=headers, dtype=dtypes,
                           skiprows=1, sep='\t+', engine='python', na_values=['\\N'], encoding='ISO-8859-1')

    chunk_list = []  # append each chunk df here
    for chunk in df_chunk:
        chunk_filter = chunk.where(pd.notnull(chunk), None)  # perform data filtering
        chunk_list.append(chunk_filter)  # Once the data filtering is done, append the chunk to list

    df_concat = pd.concat(chunk_list)  # concat the list into dataframe
    df_concat.info(memory_usage="deep")

    # solution #1
    # df = pd.DataFrame(data=df_concat)
    df_concat.to_sql(base_name, con=db.engine, index=False, index_label=None, if_exists="append")

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


def run_db_imports():
    file_names = ["name.basic", "akas", "crew", "episode", "raitings", "title_basics"]
    db_names = ["imdb_basic_name", "imdb_akas", "imdb_crew", "imdb_episode", "imdb_raitings", "imdb_title_basics"]
    headers_list = [name_basics_headers, akas_headers, crew_headers, episode_headers,
                    raitings_headers, title_basics_headers]
    dtypes_list = [name_basics_dtypes, akas_dtypes, crew_dtypes, episode_dtypes, raitings_dtypes, title_basics_dtypes]
    filepath = "C:\\Users\\GORNOSTAEVKK\\PycharmProjects\\onkin\\film_aggregator\\imdb"
    for fn, h, dt, bn in zip(file_names, headers_list, dtypes_list, db_names):
        dataset_file = "{}/{}.tsv".format(filepath, fn)
        import_dataset(dataset_file, h, dt, bn)
