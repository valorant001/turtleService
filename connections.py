import mysql.connector
from pymysql.cursors import DictCursor

# connections.py
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="turtle",
    )
    return conn

    
def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Connection closed.")

