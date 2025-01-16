import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="my_database"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
