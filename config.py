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
        self.__db = MySQL(self.__app)

    def run(self):
        self.__app.run(
            debug=True
            )

    @property
    def db(self) -> MySQL:
        return self.__db

    @property
    def app(self) -> Flask:
        return self.__app


server = Server()