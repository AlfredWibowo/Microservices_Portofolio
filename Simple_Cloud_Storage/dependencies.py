from fileinput import close
from django.dispatch import receiver
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

    def upload_file(self, uploader, file_name):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        #cheking duplicate file
        sql = "SELECT * FROM storage WHERE owner = %s AND file_name = %s"
        cursor.execute(sql, (uploader, file_name,))

        if (cursor.rowcount > 0):
            cursor.close()
            return None
        else:
            sql = "INSERT INTO storage (owner, file_name) VALUES (%s, %s)"
            cursor.execute(sql, (uploader, file_name))
            self.connection.commit()

            #check upload
            sql = "SELECT * FROM storage WHERE owner = %s AND file_name = %s"
            cursor.execute(sql, (uploader, file_name,))

            result = cursor.fetchone()

            cursor.close()
            return result

    def download_file(self, downloader, file_name):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        #check have access
        sql = "SELECT * FROM storage WHERE owner = %s AND file_name = %s"
        cursor.execute(sql, (downloader, file_name,))

        if (cursor.rowcount > 0):
            #have access
            return file_name
        else:
            #check shared or not
            
            sql = "SELECT * FROM shared WHERE receiver = %s AND file_name = %s"
            cursor.execute(sql, (downloader, file_name,))

            if (cursor.rowcount > 0):
                #shared
                return file_name
            
            else:
                cursor.close()
                return None


    def share_file(self, owner, share_to, file_name):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        #check already shared or not
        sql = "SELECT * FROM shared WHERE receiver = %s AND file_name = %s"
        cursor.execute(sql, (share_to, file_name,))

        if (cursor.rowcount > 0):
            #already shared
            cursor.close()
            return None
        else:
            #check user is exsist
            sql = "SELECT * FROM user WHERE username = %s"
            cursor.execute(sql, (share_to,))

            if (cursor.rowcount > 0):
                #check have access to share
                sql = "SELECT * FROM storage WHERE owner = %s AND file_name = %s"
                cursor.execute(sql, (owner, file_name,))

                if (cursor.rowcount > 0):
                    #have access
                    sql = "INSERT INTO shared (receiver, file_name) VALUES (%s, %s)"
                    cursor.execute(sql, (share_to, file_name))
                    self.connection.commit()

                    #check share
                    sql = "SELECT * FROM shared WHERE receiver = %s AND file_name = %s"
                    cursor.execute(sql, (receiver, file_name,))

                    result = cursor.fetchone()

                    cursor.close()
                    return result
                else:
                    #no have access
                    return 1
            else:
                #user does not exist
                cursor.close()
                return 0


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