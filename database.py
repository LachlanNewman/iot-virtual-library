'''
    Database
    LACHLAN NEWMAN
'''


import json
import psycopg2
import pandas as pd
from pandas.io import sql


class Database:
    '''
    Create an object that makes insert statements and queries
    '''
    def __init__(self, config_file):

        with open(config_file) as db_config_file:
            self._db_config = json.load(db_config_file)

        try:
            self._connection = psycopg2.connect(**self._db_config['config'])
            self._cursor = self._connection.cursor()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def create_table(self, table_name):
        '''
        Creates a table in the database if it does not already exist
        :param table_name:
        '''
        create_table_query = "CREATE TABLE IF NOT EXISTS {}(".format(table_name)
        for item in self._db_config[table_name]:
            table_value = "{key} {type},".format(**item)
            create_table_query = create_table_query + table_value
        create_table_query = create_table_query + "date Date default current_date)"
        self._cursor.execute(create_table_query)
        self._connection.commit()

    def insert(self, table_name, values: tuple):
        '''
        Insers an entry into the table in database
        :param table_name:
        :param values:
        '''
        insert_keys_query = " INSERT INTO {} (".format(table_name)
        insert_values_query = "VALUES("
        for item in self._db_config[table_name]:
            insert_key = "{key},".format(**item)
            insert_keys_query = insert_keys_query + insert_key
            insert_values_query = insert_values_query + "%s,"
        insert_keys_query = insert_keys_query[:-1] + ")"
        insert_values_query = insert_values_query[:-1] + ")"
        insert_query = insert_keys_query + insert_values_query
        self._cursor.execute(insert_query, values)
        self._connection.commit()

    def query(self, query):
        '''
        Exectutes a Query
        :param query:
        '''
        self._cursor.execute(query)
        data = sql.read_sql(query,self._connection)
        return data

    def close(self):
        '''Closes the DataBase'''
        self._cursor.close()
        self._connection.close()
