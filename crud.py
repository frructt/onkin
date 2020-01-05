import database
import sql.films_table


def get_all_films():
    query = sql.films_table.get_all_films
    return database.get_query_multiple_results(query)


def return_all_films():
    rows = get_all_films()
    films_list = []
    for row in rows:
        pass

