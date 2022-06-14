from dao import *
from config import server

class FactoryDao:
    def __init__(self, db) -> None:
        self.__user = UserDao(db)
        self.__post = PostDao(db)
        self.__friend = FriendDao(db)
        self.__code = CodeDao(db)
        self.__file = FileDao(db)
        self.__comment = CommentDao(db)
        self.__notification = NotificationDao(db)

    @property
    def user(self):
        return self.__user

    @property
    def post(self):
        return self.__post

    @property
    def friend(self):
        return self.__friend

    @property
    def code(self):
        return self.__code

    @property
    def file(self):
        return self.__file

    @property
    def comment(self):
        return self.__comment

    @property 
    def notification(self):
        return self.__notification

dao = FactoryDao(server.db)
