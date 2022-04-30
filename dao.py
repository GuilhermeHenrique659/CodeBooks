
import sqlite3
from models import Code, User, Post

SQL_FRIEND_LIST_FRIEND = 'SELECT idUser, name, image FROM Friendship join user on Friendship.Friend_idUser = user.idUser where ( User_idUser = ? or Friend_idUser = ?) and idUser != ?'

SQL_FRIEND_LIST_USER = 'SELECT idUser, name,image FROM Friendship join user on Friendship.User_idUser = user.idUser where ( User_idUser = ? or Friend_idUser = ?) and idUser != ?'

SQL_FRIEND_EXISTS = 'SELECT * FROM Friendship WHERE (User_idUser = ? and Friend_idUser = ?) or ( User_idUser = ? and Friend_idUser = ?) '

SQL_FRIEND_DELETE = 'DELETE FROM Friendship WHERE (User_idUser = ? and Friend_idUser = ?) or ( User_idUser = ? and Friend_idUser = ?) '

SQL_SEARCH_USER = 'select name, idUser, image from user where name=? and idUser !=?'

SQL_SEARCH_USER_LOGIN = 'select * from user where email=?'

SQL_CREATE_USER = 'INSERT INTO user (name, email, age, password) VALUES (?,?,0000-00-00,?)'

SQL_EDIT_USER = 'UPDATE user SET name=?,email=?,age=?,image=?,job=?,password=? WHERE idUser=?'

SQL_ADD_FRIEND = 'INSERT INTO Friendship (User_idUser,Friend_idUser) VALUES (?,?)'

SQL_LIST_POST = 'SELECT * FROM Post LEFT JOIN User ON User.idUser = Post.User_idUser'

SQL_CREATE_POST = 'INSERT INTO post (title, description, User_idUser) VALUES (?,?,?)'

SQL_EDIT_POST = 'UPDATE Post SET title=?, description=? WHERE idPost=? AND User_idUser = ?'

SQL_CREATE_CODE = 'INSERT INTO code (code, Post_idPost, User_id) VALUES (?,?,?) '

SQL_SEARCH_USER_PROFILE = 'SELECT * FROM user where idUser = ?'

SQL_SEARCH_CODE_LIST = 'SELECT code,Post_idPost,created_at,idCode,name,idUser FROM Code LEFT JOIN User ON User.idUser = code.User_id WHERE Post_idPost = ?'

SQL_DELETE_USER = 'DELETE FROM User WHERE idUser=? '

SQL_DELETE_POST = 'DELETE FROM Post WHERE idPost=? and User_idUser = ?'

SQL_DELETE_CODE = 'DELETE FROM Code WHERE idCode = ? and User_id = ?'


class FriendDao:
    def __init__(self, db) -> None:
        self.__db = db

    def user_search(self, name, iduser):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER, (name, iduser))
        users_data = self.__translate_to_list(cursor.fetchall())
        return users_data


    def friend_list(self, user_id) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_LIST_FRIEND, (user_id, user_id, user_id,))
        friend_list = self.__translate_to_list(cursor.fetchall())
        cursor.execute(SQL_FRIEND_LIST_USER, (user_id, user_id, user_id,))
        friend_list.extend(self.__translate_to_list(cursor.fetchall()))
        return friend_list

    def friend_exists(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_EXISTS,
                       (user_id, friend_id, friend_id, user_id))
        friend_list = cursor.fetchall()
        return friend_list

    def remove_friend(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_DELETE,
                    (user_id, friend_id, friend_id, user_id))
        self.__db.commit()

    def add_friend_in_db(self, friend_id, user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_ADD_FRIEND, (user_id, friend_id,))
        except NameError:
            return NameError
        self.__db.commit()
        return cursor.lastrowid

    def __translate_to_list(self, user_dict):
        def translate_to_objects(user_dict):
            return User(user_dict['name'], None, None, user_dict['idUser'],image=user_dict['image'])
        return list(map(translate_to_objects, user_dict) )

class UserDao:
    def __init__(self, db) -> None:
        self.__db = db

    def user_search_login(self, user_data) -> object:
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER_LOGIN, (user_data,))
        data_user = cursor.fetchone()
        try:
            user = User(data_user['name'], data_user['email'],
                        data_user['password'], data_user['idUser'], image=data_user['image'])
            return user
        except:
            return None

    def save_user(self, user) -> int:
        cursor = self.__db.cursor()
        try:
            if user._id:
                cursor.execute(SQL_EDIT_USER, (user._name,user._email,user._age,user._image,
                                                user._job,user._password,user._id))
            else:
                cursor.execute(SQL_CREATE_USER, (user._name,
                               user._email, user._password,))
        except sqlite3.IntegrityError as error:
            return "email not available"
        self.__db.commit()
        return cursor.lastrowid

    def search_user_profile(self, id) -> User:
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_SEARCH_USER_PROFILE, (id,))
            data_user_db = cursor.fetchone()
            return User(data_user_db['name'],data_user_db['email'],None,data_user_db['idUser'],
                            data_user_db['age'],data_user_db['image'],data_user_db['job'])
        except:
            return None

    def delete_user(self,id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETE_USER, (id,))
        self.__db.commit()



class PostDao:
    def __init__(self, db) -> None:
        self.__db = db

    def __translate_to_list(self, post_db) -> list:
        def translate_to_object(post):
            user = User(post['name'],post['email'], None, post['idUser'],image=post['image'])
            return Post(post['title'], post['description'],user,post['created_at'], 
                        post['updated_at'], post['like_cont'], post['idPost'])
        return list(map(translate_to_object, post_db))

    def list_post(self) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_POST,)
        list_post_db = cursor.fetchall()        
        try:
            list_post = self.__translate_to_list(list_post_db)
            return list_post
        except:
            return None

    def delete_post(self, post_id,user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_DELETE_POST,(post_id,user_id,))
        except NameError as error:
            return error
        self.__db.commit()

    def create_post(self,post):
        cursor = self.__db.cursor()
        try:
            if post._idPost:
                cursor.execute(SQL_EDIT_POST, (post._title,post._description, post._idPost, post._user))
            else:
                cursor.execute(SQL_CREATE_POST,(post._title, post._description, post._user,))
        except NameError:
            return None
        self.__db.commit()
        post_id = cursor.lastrowid
        return post_id
        
class CodeDao:
    def __init__(self,db) -> None:
        self.__db = db

    def create_code(self,code):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CREATE_CODE,(code._code,code._idPost,code._user,))
        except NameError:
            return None
        self.__db.commit()   
        return cursor.lastrowid

    def delete_code(self, id, user_id):
        self.__db.cursor().execute(SQL_DELETE_CODE,(id,user_id,))
        self.__db.commit()
    
    def list_code(self, id_post) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_CODE_LIST,(id_post,))
        list_code_db = cursor.fetchall()
        list_code = self.__translate_to_list(list_code_db)
        return list_code
    
    def __translate_to_list(self, code_db) -> list:
        def translate_to_object(code):
            user = User(code['name'],None,None,code['idUser'])
            return Code(code['code'],code['Post_idPost'],user,code['created_at'],code['idCode'])
        return list(map(translate_to_object, code_db))

    


        
