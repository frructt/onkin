import db_interface
import parameters


def get_query_single_result(query):
    connection = db_interface.DatabaseInterface(parameters.server, parameters.database, parameters.uid, parameters.pwd)
    result = connection.get_query_single_result(query)
    return result


def get_query_multiple_results(query):
    connection = db_interface.DatabaseInterface(parameters.server, parameters.database, parameters.uid, parameters.pwd)
    result = connection.get_query_multiple_results(query)
    return result


def insert_update_del_query(query):
    connection = db_interface.DatabaseInterface(parameters.server, parameters.database, parameters.uid, parameters.pwd)
    connection.insert_update_del_query(query)
