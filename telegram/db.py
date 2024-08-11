# db.py

import mysql.connector
from mysql.connector import Error

class SakilaDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def search_by_keyword(self, keyword, limit=10):
        query = f"SELECT title, release_year, description FROM film WHERE title LIKE %s LIMIT %s"
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (f"%{keyword}%", limit))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    def search_by_genre_and_year(self, genre, year, limit=10):
        query = f"SELECT title, release_year, description FROM film WHERE genre LIKE %s AND release_year = %s LIMIT %s"
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (f"%{genre}%", year, limit))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_popular_queries(self):

        return []
