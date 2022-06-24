from fileinput import close
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self, email, password, nrp, username):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        #check username already used or not
        sql = "SELECT * FROM user WHERE email = %s"
        cursor.execute(sql, (email,))
        
        if (cursor.rowcount > 0):
            cursor.close()
            return None
        else:
            #insert to db
            sql = "INSERT INTO mahasiswa (email, password, nrp, username,) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, password, nrp, username,))
            self.connection.commit()

            sql = "SELECT * FROM user WHERE email = %s"
            cursor.execute(sql, (email,))

            result = cursor.fetchone()
            
            cursor.close()
            return result 

    def login(self, email, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []     
        #checking username and password exsist 
        sql = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password,))

        if (cursor.rowcount > 0):
            result = cursor.fetchone()

            cursor.close()
            return result
        else:
            return None

    def upload_paper(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        return None

    def download_paper(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        return None

    def search(self):
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
                database='student_research_paper_storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())