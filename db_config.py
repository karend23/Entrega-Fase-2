#Importar las librerias
from flask import Flask
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="webapp"
    )
    return connection
