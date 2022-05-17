import sqlite3
import threading
import psycopg2
import psycopg2.extras
from flask import Flask , session, redirect, url_for
import os
from flask_socketio import SocketIO


class Server:
    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__app.secret_key='Codebooks'
        self.__app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__))+'/uploads'
        self.__db = psycopg2.connect( 
            host = "ec2-44-194-4-127.compute-1.amazonaws.com",
            user = "ifcrdmlmixptjt",
            password = "188cb6ba4bfe0100b1e1875c13df58a5368849ab59cda23fd3fa5505d5fcede5",
            port = 5432,
            database = "dell6u1d84pea2",
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        #self.__socketio = SocketIO(self.__app)

    def __dictionary_cursor(self, cursor, row):
        dictionary = {}
        for index, col in enumerate(cursor.description):
            dictionary[col[0]] = row[index]
        return dictionary

    def run(self):
        self.__app.run()
        #self.__socketio.run(self.__app)

    def loggin_required(self, controller):
        def wrapper(*agrs, **kwargs):
            if 'login_user' not in session or session['login_user'] == None:
                return redirect(url_for('login'))
            return controller(*agrs, **kwargs)
        return wrapper

    @property
    def db(self) -> psycopg2:
        return self.__db

    @property
    def app(self) -> Flask:
        return self.__app

    @property
    def socketio(self):
        return self.__socketio

server = Server()