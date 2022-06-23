import json
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self, username, password):
        cursor = self.connection.cursor(dictionary=True,buffered=True)
        result = []

        #check username already used or not
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql, (username,))

        if (cursor.rowcount == 0):  
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password,))
            sql2 = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(sql2, (username, password,))
            result = cursor.fetchone()
            cursor.close()
            self.connection.commit()
            return result
        else:
            cursor.close()
            return None

    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='127.0.0.1',
                database='department_news_board',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())