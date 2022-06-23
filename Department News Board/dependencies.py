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
        cursor = self.connection.cursor(dictionary=True)
        result = []

        #check username already used or not
        sql = "SELECT * FROM user WHERE username = %s"
        cursor.execute(sql, (username,))
        
        if (cursor.rowcount == 0):
            #insert to db
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password,))
            self.connection.commit()
            
            sql = "SELECT * FROM user WHERE username = %s AND password %s"
            cursor.execute(sql, (username, password))

            if (cursor.rowcount > 0):
                row = cursor.fetchone()
                result.append({
                    'username': row['username'],
                    'password': row['password'],
                })
            
            cursor.close()
            return result
        else:
            return None

    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []     
        #checking username and password exsist 
        sql = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password,))

        if (cursor.rowcount > 0):
            row = cursor.fetchone()
            result.append({
                'username': row['username'],
                'password': row['password'],
            })

            cursor.close()
            return result
        else:
            return None

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news"
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            for row in cursor.fetchall():
                result.append({
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'desc': row['desc'],
                }) 
                
                cursor.close()
                return result
        else:
            return None

    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        if (cursor.rowcount > 0):
            row = cursor.fetchone()
            result.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'desc': row['desc'],
            })

            cursor.close()
            return result
        else:
            return None

    def add_news(self, desc):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "INSERT INTO news (date, desc) VALUES (CURRENT_DATE, %s)"
        cursor.execute(sql, (desc,))
        self.connection.commit()

        #check add
        sql = "SELECT * FROM news ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        
        if (cursor.rowcount > 0):
            lastrow = cursor.fetchone()
            result.append({
                'id': lastrow['id'],
                'timestamp': lastrow['timestamp'],
                'desc': lastrow['desc'],
            })
            
            cursor.close()
            return result
        else:
            return None

    def edit_news(self, news_id, desc):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "UPDATE news (date, description) VALUES (CURRENT_DATE, %s) WHERE id = %s"
        cursor.execute(sql, (desc, news_id))
        self.connection.commit()
        
        #check edit
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        if (cursor.rowcount > 0):
            row = cursor.fetchone()
            result.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'desc': row['desc'],
            })

            cursor.close()
            return result
        else:
            return None

    def delete_news(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "DELETE FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        #check
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        if (cursor.rowcount > 0):
            result = False
        else:
            result = True

        cursor.close()
        return result

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