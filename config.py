import psycopg2
import psycopg2.extras
from flask import Flask , session, redirect, url_for
import os
from os import environ
from dotenv import load_dotenv
from flask_socketio import SocketIO




class Server:
    def __init__(self) -> None:
        load_dotenv()
        self.__app = Flask(environ.get("FLASK_APP"))
        self.__app.secret_key=os.getenv("SECRET_KEY")
        self.__app.config["DEBUG"] = os.getenv("FLASK_DEBUG")
        self.__app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__))+'/uploads'
        self.__db = psycopg2.connect( 
            host = environ.get("POSTGRESQL_HOST"),
            user =  environ.get("POSTGRESQL_USER"),
            password =  environ.get("POSTGRESQL_PASSWORD"),
            port =  environ.get("POSTGRESQL_PORT"),
            database =  environ.get("POSTGRESQL_DATABASE"),
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        self.__socketio = SocketIO(self.__app)

    def transaction(self, methotd):
        def wrapper(*agrs, **kwargs):
            try:
                return methotd(*agrs, **kwargs)
            except Exception as error:
                self.__db.rollback()
        return wrapper

    def run(self):
        self.__app.run(debug=True)

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