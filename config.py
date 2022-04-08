import sqlite3
from flask import Flask
import os


class Server:
    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__app.secret_key='Codebooks'
        self.__app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__))+'\\uploads'
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