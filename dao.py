from psycopg2.errors import UniqueViolation
import psycopg2
from models import Code, User, Post, File, Comment
from config import server

SQL_FRIEND_LIST = '''
                SELECT iduser, name, image FROM Friendship 
                join users on Friendship.Friend_iduser = users.iduser 
                where ( User_idUser = %(id_user)s or Friend_idUser = %(id_user)s) and iduser != %(id_user)s
                union
                SELECT iduser, name,image FROM Friendship 
                join users on Friendship.User_idUser = users.iduser 
                where ( User_idUser = %(id_user)s or Friend_idUser = %(id_user)s) and iduser != %(id_user)s
'''

SQL_FRIEND_EXISTS = 'SELECT * FROM Friendship WHERE (User_idUser = %(id_user)s and Friend_idUser = %(id_friend)s) or ( User_idUser = %(id_friend)s and Friend_idUser = %(id_user)s) '

SQL_FRIEND_DELETE = 'DELETE FROM Friendship WHERE (User_idUser = %(id_user)s and Friend_idUser = %(id_friend)s) or ( User_idUser = %(id_friend)s and Friend_idUser = %(id_user)s) '

SQL_SEARCH_USER = 'select name, iduser, image from users where name ilike %s and iduser !=%s'

SQL_SEARCH_USER_LOGIN = 'select * from users where email=%s'

SQL_CREATE_USER = "INSERT INTO users (name, email, age, password) VALUES (%s,%s,'1996-12-02',%s)"

SQL_EDIT_USER = 'UPDATE users SET name=%s,email=%s,age=%s,image=%s,job=%s,password=%s WHERE iduser=%s'

SQL_ADD_FRIEND = 'INSERT INTO Friendship (User_iduser,Friend_iduser) VALUES (%s,%s)'

SQL_LIST_POST = '''
                SELECT title, description,like_cont, created_at, updated_at,idPost, name, idUser,email, image  
                FROM Post 
                LEFT JOIN users ON users.idUser = Post.User_idUser
'''

SQL_CREATE_POST = 'INSERT INTO post (title, description, User_iduser) VALUES (%s,%s,%s) RETURNING idPost'

SQL_EDIT_POST = 'UPDATE Post SET title=%s, description=%s WHERE idPost=%s AND User_iduser = %s RETURNING idPost'

SQL_CREATE_CODE = 'INSERT INTO code (code, Post_idPost, User_id) VALUES (%s,%s,%s) '

SQL_SEARCH_USER_PROFILE = 'SELECT * FROM users where iduser = %s'

SQL_SEARCH_CODE_LIST = 'SELECT code,Post_idPost,created_at,idCode,name,iduser FROM Code LEFT JOIN users ON users.iduser = code.User_id WHERE Post_idPost = %s'

SQL_DELETE_USER = 'DELETE FROM users WHERE iduser=%s '

SQL_DELETE_POST = 'DELETE FROM Post WHERE idPost=%s and User_iduser = %s'

SQL_DELETE_CODE = 'DELETE FROM Code WHERE idCode = %s and User_id = %s'

SQL_CREATE_FILE = 'INSERT INTO files (file,type,idPost) VALUES (%s,%s,%s)'

SQL_LIST_FILE = 'SELECT file, type, idPost FROM Files WHERE idPost = %s'

SQL_DELETE_FILE = 'DELETE FROM files WHERE idPost = %s'

SQL_INSERT_COMMENT = 'INSERT INTO comment (Comment, Post_idPost, User_iduser) VALUES (%s,%s,%s) RETURNING idcomment'

SQL_LIST_COMMENT = 'SELECT idComment, Comment, Post_idPost, User_iduser, name, image FROM Comment JOIN users ON users.iduser = Comment.User_iduser WHERE Post_idPost = %s'



class FriendDao:
    def __init__(self, db:psycopg2) -> None:
        self.__db = db

    @server.transaction
    def user_search(self, name, iduser):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER, (name, iduser))
        users_data = self.__translate_to_list(cursor.fetchall())
        return users_data


    @server.transaction
    def friend_list(self, user_id) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_LIST, {'id_user': user_id})
        friend_list = self.__translate_to_list(cursor.fetchall())
        return friend_list


    @server.transaction
    def friend_exists(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_EXISTS, {'id_user':user_id, 'id_friend': friend_id})
        friend_list = cursor.fetchall()
        return friend_list

    @server.transaction
    def remove_friend(self, friend_id, user_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FRIEND_DELETE, {'id_user':user_id, 'id_friend': friend_id})
        self.__db.commit()

    @server.transaction
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
            return User(user_dict['name'], None, None, user_dict['iduser'],image=user_dict['image'])
        return list(map(translate_to_objects, user_dict) )

class UserDao:
    def __init__(self, db:psycopg2) -> None:
        self.__db = db


    @server.transaction
    def user_search_login(self, user_data) -> User:
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER_LOGIN, (user_data,))
        data_user = cursor.fetchone()
        user = self.create_user_object(data_user) if data_user else None
        return user

    def create_user_object(self, data_user):
        user = User(data_user['name'], data_user['email'],
                        data_user['password'], data_user['iduser'], image=data_user['image'])
                        
        return user


    @server.transaction
    def save_user(self, user:User):
        cursor = self.__db.cursor()
        try:
            if user._id:
                cursor.execute(SQL_EDIT_USER, (user._name,user._email,user._age,user._image,
                                                user._job,user._password,user._id))
            else:
                cursor.execute(SQL_CREATE_USER, (user._name,
                               user._email, user._password,))
        except UniqueViolation as error:
            print(error)
            return "email not available"
        self.__db.commit()
        return cursor.lastrowid

    @server.transaction
    def search_user_profile(self, id) -> User:
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_USER_PROFILE, (id,))
        data_user_db = cursor.fetchone()
        return User(data_user_db['name'],data_user_db['email'],None,data_user_db['iduser'],
                            data_user_db['age'],data_user_db['image'],data_user_db['job'])

    @server.transaction
    def delete_user(self,id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_DELETE_USER, (id,))
        self.__db.commit()



class PostDao:
    def __init__(self, db:psycopg2) -> None:
        self.__db = db

    def __translate_to_list(self, post_db) -> list:
        def translate_to_object(post) -> Post:
            user = User(post['name'],post['email'], None, post['iduser'],image=post['image'])
            return Post(post['title'], post['description'],user,post['created_at'], 
                        post['updated_at'], post['like_cont'], post['idpost'])
        return list(map(translate_to_object, post_db))

    @server.transaction
    def list_post(self) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_POST)
        post_list = self.__translate_to_list(cursor.fetchall())
        return post_list  

    @server.transaction
    def delete_post(self, post_id,user_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_DELETE_POST,(post_id,user_id,))
        except NameError as error:
            return error
        self.__db.commit()

    @server.transaction
    def create_post(self,post:Post):
        cursor = self.__db.cursor()
        
        if post._idPost:
                cursor.execute(SQL_EDIT_POST, (post._title,post._description, post._idPost, post._user))
        else:
                cursor.execute(SQL_CREATE_POST,(post._title, post._description, post._user,))
        self.__db.commit()
        post_id = cursor.fetchone()['idpost']
        return post_id
        
class CodeDao:
    def __init__(self,db:psycopg2) -> None:
        self.__db = db

    @server.transaction
    def create_code(self,code:Code):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CREATE_CODE,(code._code,code._idPost,code._user,))
        except NameError:
            return None
        self.__db.commit()   
        return cursor.lastrowid

    @server.transaction
    def delete_code(self, id, user_id):
        self.__db.cursor().execute(SQL_DELETE_CODE,(id,user_id,))
        self.__db.commit()
    
    @server.transaction
    def list_code(self, id_post) -> list:
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_CODE_LIST,(id_post,))
        list_code_db = cursor.fetchall()
        list_code = self.__translate_to_list(list_code_db)
        return list_code

    
    def __translate_to_list(self, code_db) -> list:
        def translate_to_object(code) -> Code:
            user = User(code['name'],None,None,code['iduser'])
            return Code(code['code'],code['post_idpost'],user,code['created_at'],code['idcode'])
        return list(map(translate_to_object, code_db))

class FileDao:
    def __init__(self,db:psycopg2) -> None:
        self.__db = db
    
    @server.transaction
    def save_files(self, file:File):
        cursor = self.__db.cursor()
        cursor.execute(SQL_CREATE_FILE,(file._filename,file._type,file._id_post) )
        self.__db.commit()

    @server.transaction
    def findall_files(self, idpost):
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_FILE,(idpost,))
        files_list = self.translate_to_list(cursor.fetchall())
        if len(files_list) == 0:
            return None
        return files_list

    @server.transaction
    def delete_files(self, idpost):
        self.__db.cursor().execute(SQL_DELETE_FILE,(idpost,))
        self.__db.commit()



    def translate_to_list(self, files_db) -> list :
        def translate_to_object(file) -> File:
            return File(file['file'],file['type'],file['idpost'])
        file_list = list(map(translate_to_object, files_db))
        return file_list

        
class CommentDao:
    def __init__(self,db:psycopg2) -> None:
        self.__db = db

    @server.transaction
    def save_comment(self, comment: Comment):
        cursor = self.__db.cursor()
        if comment._idComment:
            pass
        else:
            sql = cursor.execute(SQL_INSERT_COMMENT, (comment._Comment, comment._idPost, comment._idUser))
            print(sql)
        self.__db.commit()
    
    def __translate_to_list(self, comment_db) -> list:
        def translate_to_object(comment):
            user = User(comment['name'], None, None, comment['user_iduser'], image=comment['image'])
            return Comment(comment['comment'], comment['post_idpost'], user, comment['idcomment'])
        return list(map(translate_to_object, comment_db))
    
    @server.transaction
    def list_comment(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_LIST_COMMENT,(id,))
        listDb = cursor.fetchall()
        return self.__translate_to_list(listDb)
