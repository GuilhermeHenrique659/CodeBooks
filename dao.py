import sqlite3
from models import User

SQL_FRIEND_LIST_FRIEND = 'SELECT * FROM Friendship join user on Friendship.Friend_idUser = user.idUser where ( User_idUser = ? or Friend_idUser = ?) and idUser != ?'
SQL_FRIEND_LIST_USER = 'SELECT * FROM Friendship join user on Friendship.User_idUser = user.idUser where ( User_idUser = ? or Friend_idUser = ?) and idUser != ?'
SQL_FRIEND_EXISTS = 'SELECT * FROM Friendship WHERE (User_idUser = ? and Friend_idUser = ?) or ( User_idUser = ? and Friend_idUser = ?) '
SQL_SEARCH_USER = 'select name, idUser from user where name=? and idUser !=?'
SQL_SEARCH_USER_LOGIN = 'select * from user where email=?'
SQL_CREATE_USER = 'INSERT INTO user (name, email, age, password) VALUES (?,?,0000-00-00,?)'
SQL_ADD_FRIEND = 'INSERT INTO Friendship (User_idUser,Friend_idUser) VALUES (?,?)'

class FriendDao:
    def __init__(self,db) -> None:
        self.__db = db

    def user_search(self, name, iduser):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER, (name,iduser) )
        users_data = self.translate_to_list(cursor.fetchall())
        return users_data

    def friend_list(self, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_LIST_FRIEND, (user_id,user_id,user_id,) )
        friend_list = self.translate_to_list(cursor.fetchall())
        cursor.execute(SQL_FRIEND_LIST_USER, (user_id,user_id,user_id,) )
        friend_list.extend(self.translate_to_list(cursor.fetchall()))
        return friend_list

    def friend_exists(self, friend_id,user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_EXISTS, (user_id,friend_id,friend_id,user_id))
        friend_list = cursor.fetchall()
        return friend_list

    def add_friend_in_db(self, friend_id,user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_ADD_FRIEND,(user_id,friend_id,))
        except NameError:
            return NameError
        self.__db.commit()
        return cursor.lastrowid

    def translate_to_list(self, user_dict):
        def translate_to_objects(user_dict):
            return User(user_dict['name'], None, None, user_dict['idUser'])
        return list(map(translate_to_objects, user_dict))

class UserDao:
    def __init__(self, db) -> None:
        self.__db = db

    def user_search_login(self,user_data):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER_LOGIN, (user_data,) )
        data = cursor.fetchone()
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
            return "email not available"
        self.__db.commit()
        return cursor.lastrowid


    