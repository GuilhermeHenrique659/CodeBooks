from errno import errorcode
from tkinter import E

import MySQLdb
from models import User

SQL_SEARCH_USER_LOGIN = 'select * from user where email=%s'
SQL_CREATE_USER = 'INSERT INTO user (name, email, age, password) VALUES (%s,%s,0000-00-00,%s)'

class UserDao:
    def __init__(self, db) -> None:
        self.__db = db

    def user_search_login(self,user_data):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SEARCH_USER_LOGIN, (user_data,) )
        data = cursor.fetchone()
        try:
            user = User(data['name'],data['email'],data['password'],data['idUser'])
            return user
        except:
            return None
        
    def create_user(self,user):
        cursor = self.__db.connection.cursor()
        try:
            if user._id:
                pass
            else:
                cursor.execute(SQL_CREATE_USER,(user._name,user._email,user._password,) )
        except MySQLdb.IntegrityError as error:
            print(error)
            return error.args[0]
        cursor._id = cursor.lastrowid
        self.__db.connection.commit()
        return cursor._id


    