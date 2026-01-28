import sqlite3 

connection = sqlite3.connect('books.db')


cursor = connection.cursor()

sql = '''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INTEGER
)
'''

cursor.execute(sql)

connection.commit()
connection.close()
