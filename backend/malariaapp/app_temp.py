from flask import Flask, jsonify, request, make_response
import sqlite3
import datetime
import jwt

from core import create_app
from config import Config


def db_connection():
    connection = sqlite3.connect('books.db')
    return connection

app = create_app()






@app.route('/protected', methods=['GET'])
def protected():
    token = None
    if 'x-access-token' in request.headers: 
        token = request.headers['x-access-token']
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        current_user = data['payload']      
        return jsonify({'message': f'Welcome {current_user} to the protected route!'})
    except:
        return jsonify({'message': 'Token is invalid!'}), 401




@app.route('/unprotected', methods=['GET'])
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/login')
def login():
    # jwt token generation logic will go here
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({"payload": auth.username}, Config.SECRET_KEY,algorithm="HS256")
        return  jsonify({'token': token})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/books', methods=['GET', 'POST'])
def books():
    connection=db_connection()
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        return jsonify(books)
    elif request.method == 'POST':
        new_book = request.get_json()
        print(new_book)
        cursor.execute('INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)',
                       (new_book['title'], new_book['author'], new_book['published_year']))
       
        connection.commit()       
        return jsonify(new_book), 201


@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    connection = db_connection()
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM books WHERE id=?', (id,))
        book = cursor.fetchone()
        if book:
            return jsonify(book)
        else:
            return jsonify({'message': 'Book not found'}), 404
    elif request.method == 'PUT':
        updated_book = request.get_json()
        cursor.execute('SELECT * FROM books WHERE id=?', (id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({'message': 'Book not found'}), 404



        cursor.execute('UPDATE books SET title=?, author=?, published_year=? WHERE id=?',
                       (updated_book['title'], updated_book['author'], updated_book['published_year'], id))
        connection.commit()
        return jsonify(updated_book)
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM books WHERE id=?', (id,))
        connection.commit()
        return jsonify({'message': 'Book deleted'})


if __name__ == '__main__':
    app.run(debug=True) 