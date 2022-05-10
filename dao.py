
import sqlite3
from models import Code, User, Post, File, Comment


SQL_FRIEND_LIST = '''
                SELECT idUser, name, image FROM Friendship 
                join user on Friendship.Friend_idUser = user.idUser 
                where ( User_idUser = :id_user or Friend_idUser = :id_user) and idUser != :id_user
                union
                SELECT idUser, name,image FROM Friendship 
                join user on Friendship.User_idUser = user.idUser 
                where ( User_idUser = :id_user or Friend_idUser = :id_user) and idUser != :id_user
'''

SQL_FRIEND_EXISTS = 'SELECT * FROM Friendship WHERE (User_idUser = :id_user and Friend_idUser = :id_friend) or ( User_idUser = :id_friend and Friend_idUser = :id_user) '

SQL_FRIEND_DELETE = 'DELETE FROM Friendship WHERE (User_idUser = :id_user and Friend_idUser = :id_friend) or ( User_idUser = :id_friend and Friend_idUser = :id_user) '

SQL_SEARCH_USER = 'select name, idUser, image from user where name=? and idUser !=?'

SQL_SEARCH_USER_LOGIN = 'select * from user where email=?'

SQL_CREATE_USER = 'INSERT INTO user (name, email, age, password) VALUES (?,?,0000-00-00,?)'

SQL_EDIT_USER = 'UPDATE user SET name=?,email=?,age=?,image=?,job=?,password=? WHERE idUser=?'

SQL_ADD_FRIEND = 'INSERT INTO Friendship (User_idUser,Friend_idUser) VALUES (?,?)'

SQL_LIST_POST = 'SELECT title, description,like_cont, created_at, updated_at,idPost, name, idUser,email, image  FROM Post LEFT JOIN User ON User.idUser = Post.User_idUser'

SQL_CREATE_POST = 'INSERT INTO post (title, description, User_idUser) VALUES (?,?,?)'

SQL_EDIT_POST = 'UPDATE Post SET title=?, description=? WHERE idPost=? AND User_idUser = ?'

SQL_CREATE_CODE = 'INSERT INTO code (code, Post_idPost, User_id) VALUES (?,?,?) '

SQL_SEARCH_USER_PROFILE = 'SELECT * FROM user where idUser = ?'

SQL_SEARCH_CODE_LIST = 'SELECT code,Post_idPost,created_at,idCode,name,idUser FROM Code LEFT JOIN User ON User.idUser = code.User_id WHERE Post_idPost = ?'

SQL_DELETE_USER = 'DELETE FROM User WHERE idUser=? '

SQL_DELETE_POST = 'DELETE FROM Post WHERE idPost=? and User_idUser = ?'

SQL_DELETE_CODE = 'DELETE FROM Code WHERE idCode = ? and User_id = ?'

SQL_CREATE_FILE = 'INSERT INTO files (file,type,idPost) VALUES (?,?,?)'

SQL_LIST_FILE = 'SELECT file, type, idPost FROM Files WHERE idPost = ?'

SQL_DELETE_FILE = 'DELETE FROM files WHERE idPost = ?'

SQL_INSERT_COMMENT = 'INSERT INTO comment (Comment, Post_idPost, User_idUser) VALUES (?,?,?)'

SQL_LIST_COMMENT = 'SELECT idComment, Comment, Post_idPost, User_idUser, name, image FROM Comment JOIN User ON User.idUser = Comment.User_idUser WHERE Post_idPost = ?'


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
        cursor.execute(SQL_FRIEND_LIST, {'id_user':user_id})
        friend_list = self.__translate_to_list(cursor.fetchall())
        return friend_list

    def friend_exists(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_EXISTS, {'id_user':user_id, 'id_friend': friend_id})
        friend_list = cursor.fetchall()
        return friend_list

    def remove_friend(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_DELETE, {'id_user':user_id, 'id_friend': friend_id})
        self.__db.commit()

    def add_friend_in_db(self, friend_id, user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_ADD_FRIEND, (user_id, friend_id,))
        except NameError:
            return NameError
        self.__db.commit()
        return cursor.lastrowid

    def __translate_to_list(self, user_dict) -> list:
        def translate_to_objects(user_dict) -> User:
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

    def save_user(self, user:User):
        cursor = self.__db.cursor()
        try:
            if user._id:
                cursor.execute(SQL_EDIT_USER, (user._name,user._email,user._age,user._image,
                                                user._job,user._password,user._id))
            else:
                cursor.execute(SQL_CREATE_USER, (user._name,
                               user._email, user._password,))
        except sqlite3.IntegrityError:
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
        def translate_to_object(post) -> Post:
            user = User(post['name'],post['email'], None, post['idUser'],image=post['image'])
            return Post(post['title'], post['description'],user,post['created_at'], 
                        post['updated_at'], post['like_cont'], post['idPost'])
        return list(map(translate_to_object, post_db))

    def list_post(self) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_POST,)
        return  self.__translate_to_list(cursor.fetchall())        

    def delete_post(self, post_id,user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_DELETE_POST,(post_id,user_id,))
        except NameError as error:
            return error
        self.__db.commit()

    def create_post(self,post:Post):
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

    def create_code(self,code:Code):
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
        def translate_to_object(code) -> Code:
            user = User(code['name'],None,None,code['idUser'])
            return Code(code['code'],code['Post_idPost'],user,code['created_at'],code['idCode'])
        return list(map(translate_to_object, code_db))

class FileDao:
    def __init__(self,db) -> None:
        self.__db = db
    
    def save_files(self, file:File):
        cursor = self.__db.cursor()
        cursor.execute(SQL_CREATE_FILE,(file._filename,file._type,file._id_post) )
        self.__db.commit()

    def findall_files(self, idpost):
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_FILE,(idpost,))
        files_list = self.translate_to_list(cursor.fetchall())
        if len(files_list) == 0:
            return None
        return files_list

    def delete_files(self, idpost):
        self.__db.cursor().execute(SQL_DELETE_FILE,(idpost,))
        self.__db.commit()

    def translate_to_list(self, files_db) -> list :
        def translate_to_object(file) -> File:
            return File(file['file'],file['type'],file['idPost'])
        file_list = list(map(translate_to_object, files_db))
        return file_list

        
class CommentDao:
    def __init__(self,db) -> None:
        self.__db = db
    def save_comment(self, comment):
        cursor = self.__db.cursor()
        if comment._idComment:
            pass
        else:
            cursor.execute(SQL_INSERT_COMMENT, (comment._Comment, comment._idPost, comment._idUser))
        self.__db.commit()
    
    def __translate_to_list(self, comment_db) -> list:
        def translate_to_object(comment):
            user = User(comment['name'], None, None, comment['User_idUser'], image=comment['image'])
            return Comment(comment['Comment'], comment['Post_idPost'], user, comment['idComment'])
        return list(map(translate_to_object, comment_db))
    
    def list_comment(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_COMMENT,(id,))
        listDb = cursor.fetchall()
        return self.__translate_to_list(listDb)
