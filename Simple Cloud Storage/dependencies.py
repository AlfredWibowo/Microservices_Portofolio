from fileinput import close
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        #check username already used or not
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql, (username,))
        
        if (cursor.rowcount > 0):
            cursor.close()
            return None
        else:
            #insert to db
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password,))
            self.connection.commit()

            sql = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password,))

            result = cursor.fetchone()
            
            cursor.close()
            return result 

    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []     
        #checking username and password exsist 
        sql = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password,))

        if (cursor.rowcount > 0):
            result = cursor.fetchone()

            cursor.close()
            return result
        else:
            return None

    def upload_file(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        return None

    def download_file(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        return None

    def share_file(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
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
                database='simple_cloud_storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())