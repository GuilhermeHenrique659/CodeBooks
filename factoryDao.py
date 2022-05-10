from dao import *
from config import server

class FactoryDao:
    def __init__(self) -> None:
        self.__user = UserDao(server.db)
        self.__post = PostDao(server.db)
        self.__friend = FriendDao(server.db)
        self.__code = CodeDao(server.db)
        self.__file = FileDao(server.db)

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

dao = FactoryDao()
