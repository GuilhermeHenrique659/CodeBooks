import sqlite3
from flask import Flask
from flask_mysqldb import MySQL


class Server:
    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__app.secret_key='Codebooks'
        self.__app.config['MYSQL_HOST'] = '127.0.0.1'
        self.__app.config['MYSQL_USER'] = 'root'
        self.__app.config['MYSQL_PASSWORD'] = ''
        self.__app.config['MYSQL_DB'] = 'codebooksdb'
        self.__app.config['MYSQL_PORT'] = 3306
        self.__app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        #self.__db = MySQL(self.__app)
        self.__db = sqlite3.connect('db.sqlite', check_same_thread=False)

    def __dictionary_cursor(self, cursor, row):
        dictionary = {}
        for index, col in enumerate(cursor.description):
            dictionary[col[0]] = row[index]
        return dictionary

    def run(self):
        self.__app.run(
            debug=True
            )

    @property
    def db(self) -> sqlite3:
        self.__db.row_factory = self.__dictionary_cursor
        return self.__db

    @property
    def app(self) -> Flask:
        return self.__app


server = Server()