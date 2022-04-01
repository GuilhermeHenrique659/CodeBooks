import sqlite3
from models import User

SQL_SEARCH_USER_LOGIN = 'select * from user where email=?'
SQL_CREATE_USER = 'INSERT INTO user (name, email, age, password) VALUES (?,?,0000-00-00,?)'

class UserDao:
    def __init__(self, db) -> None:
        self.__db = db

    def user_search_login(self,user_data):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER_LOGIN, (user_data,) )
        data = cursor.fetchone()
        print(data)
        try:
            user = User(data['name'],data['email'],data['password'],data['idUser'])
            return user
        except:
            return None
        
    def create_user(self,user):
        cursor = self.__db.cursor()
        try:
            if user._id:
                pass
            else:
                cursor.execute(SQL_CREATE_USER,(user._name,user._email,user._password,) )
        except sqlite3.IntegrityError as error:
            print(error)
            return error.args[0]
        self.__db.commit()
        return cursor.lastrowid


    