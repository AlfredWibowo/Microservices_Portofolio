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

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        #asumsi archive = tidak dapat dilihat lg tp msh ada datanya
        sql = "SELECT * FROM news WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)"
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            for row in cursor.fetchall():
                result.append({
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'description': row['description'],
                }) 
                
            cursor.close()
            return result
        else:
            return None

    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        #asumsi archive news bisa dilihat
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        if (cursor.rowcount > 0):
            result = cursor.fetchone()

            cursor.close()
            return result
        else:
            return None

    def add_news(self, description):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "INSERT INTO news (timestamp, description) VALUES (CURRENT_DATE, %s)"
        cursor.execute(sql, (description,))
        self.connection.commit()

        #check add
        sql = "SELECT * FROM news ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        
        if (cursor.rowcount > 0):
            result = cursor.fetchone()
            
            cursor.close()
            return result
        else:
            return False

    def edit_news(self, news_id, description):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = """
            UPDATE news
            SET timestamp = CURRENT_DATE, description = %s
            WHERE id = %s
        """
        cursor.execute(sql, (description, news_id))
        self.connection.commit()
        
        #check edit
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))

        if (cursor.rowcount > 0):
            result = cursor.fetchone()

            cursor.close()
            return result
        else:
            return None

    def delete_news(self, news_id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        #check delete
        sql = "SELECT * FROM news WHERE id = %s"
        cursor.execute(sql, (news_id,))
        
        if (cursor.rowcount > 0):
            sql = "DELETE FROM news WHERE id = %s"
            cursor.execute(sql, (news_id,))
            self.connection.commit()
            cursor.close()

            return news_id
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