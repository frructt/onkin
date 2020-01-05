import pyodbc


class DatabaseInterface(object):
    def __init__(self, server, database, uid, pwd):
        self.driver = '{SQL Server}'
        self.server = server
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.connection = \
            pyodbc.connect('driver=%s;'
                           'server=%s;'
                           'database=%s;'
                           'uid=%s;'
                           'pwd=%s' % (self.driver, self.server, self.database, self.uid, self.pwd))
        self.cursor = None

    def __del__(self):
        if self.connection:
            self.connection.close()

    def __exit__(self, *args):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_query_single_result(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # del self.cursor
        self.cursor.close()
        self.cursor = None
        if result:
            return result[0]
        else:
            return result

    def get_query_multiple_results(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        del self.cursor
        self.cursor = None
        records = []
        for row in result:
            records.append(row)
        return records

    def insert_update_del_query(self, query):
        try:
            status_msg = "result returned. {} row(s) affected."
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                row_count = self.cursor.rowcount
                print(status_msg.format(row_count))
            except pyodbc.Error as ex:
                if ex.args[0] == "23000":
                    print("The same key has already been in the table")
                if ex.args[0] == "22001":
                    print("The importing data won’t fit into the column")
                    print(ex.args)
            try:
                # this loop is added cause of large batch of sql statements
                # see: https://github.com/mkleehammer/pyodbc/issues/262
                while self.cursor.nextset():
                    row_count = self.cursor.rowcount
                    print(status_msg.format(row_count))
                self.cursor.commit()
                # time.sleep(2)
            except pyodbc.Error as ex:
                print(ex)
        finally:
            # del self.cursor
            self.cursor.close()
            self.cursor = None

    # def schema_dict(self):
    #     self.cursor.execute(
    #         "SELECT sys.objects.name, sys.columns.name FROM sys.objects "
    #         "INNER JOIN sys.columns ON sys.objects.object_id = sys.columns. object_id WHERE sys.objects.type = 'U';")
    #     schema = {}
    #
    #     for it in self.cursor.fetchall():
    #         if it[0] not in schema:
    #             schema[it[0]] = {'scheme': []}
    #         else:
    #             schema[it[0]]['scheme'].append(it[1])
    #
    #     return schema
    #
    # def populate_dict(self, schema, query):
    #     for i in schema.keys():
    #         self.cursor.execute(query.format(table=i))
    #
    #         for row in self.cursor.fetchall():
    #             colindex = 0
    #
    #             for col in schema[i]['scheme']:
    #                 if not 'data' in schema[i]:
    #                     schema[i]['data'] = []
    #
    #                 schema[i]['data'].append(row[colindex])
    #                 colindex += 1
    #
    #     return schema
    #
    # def database_to_dict(self, query):
    #     self.cursor = self.connection.cursor()
    #     schema = self.populate_dict(self.schema_dict(), query)
    #     return schema

    def db_to_dict(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
