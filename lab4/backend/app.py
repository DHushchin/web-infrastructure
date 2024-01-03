import flask
import psycopg2
from flask import Flask, request
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

postgres_conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=postgres port=5432")
postgres_cursor = postgres_conn.cursor(cursor_factory=RealDictCursor)

mongo_client = MongoClient('mongo', 27017)
mongo_db = mongo_client.library


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/get-sql-library', methods=['GET'])
def get_sql_library():
    postgres_cursor.execute("SELECT * FROM books")
    books = postgres_cursor.fetchall()
    response = flask.jsonify(books)
    return response


@app.route('/create-sql-book', methods=['POST'])
def create_sql_book():
    title = request.json['title']
    genre = request.json['genre']

    postgres_cursor.execute("INSERT INTO books (title, genre) VALUES (%s, %s)", (title, genre))
    postgres_conn.commit()

    response = flask.jsonify({'title': title, 'genre': genre})
    return response


@app.route('/delete-sql-book/<book_id>', methods=['DELETE'])
def delete_sql_book(book_id):
    postgres_cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    postgres_conn.commit()

    response = flask.jsonify({'id': book_id})
    return response


@app.route('/get-nosql-library', methods=['GET'])
def get_nosql_library():
    books = mongo_db.books.find()
    response =  MongoJSONEncoder().encode(list(books))
    return response


@app.route('/create-nosql-book', methods=['POST'])
def create_nosql_book():
    title = request.json['title']
    genre = request.json['genre']

    mongo_db.books.insert_one({'title': title, 'genre': genre})

    response = flask.jsonify({'title': title, 'genre': genre})
    return response


@app.route('/delete-nosql-book/<book_id>', methods=['DELETE'])
def delete_nosql_book(book_id):
    mongo_db.books.delete_one({'_id': ObjectId(book_id)})

    response = flask.jsonify({'id': book_id})
    return response
