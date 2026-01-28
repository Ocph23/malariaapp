import sqlite3

connection = sqlite3.connect('books.db')

def db_connection():
    return connection