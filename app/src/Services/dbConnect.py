import mysql.connector
from mysql.connector import Error

def conexionBd():
    try:
        connection = mysql.connector.connect(host='localhost', port="3306", database='proyecto', user='root', password='password')
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
