from .systemcontrollers import ControllerLogin,ControllerRegister, ControllerUploads
from .feedcontrollers import ControllerFeed
from .friendcontroller import ControllerFriend
from .postcontrollers import ControllerPost
from .usercontrollers import ControllerUser
from .codecontrolles import  ControllerCode
from .chatcontrollers import ControllerChat
from .commentcontroller import ControllerComment
from .notificationcontrollers import ControllerNotification

class FactoryController:
    def __init__(self) -> None:
        self.__login = ControllerLogin()
        self.__register = ControllerRegister()
        self.__uploads = ControllerUploads()
        self.__feed = ControllerFeed()
        self.__friend = ControllerFriend()
        self.__post = ControllerPost()
        self.__user = ControllerUser()
        self.__code = ControllerCode()
        self.__chat = ControllerChat()
        self.__comment = ControllerComment()
        self.__notification = ControllerNotification()

    @property
    def login(self):
        return self.__login

    @property
    def register(self):
        return self.__register

    @property
    def uploads(self):
        return self.__register
    
    @property
    def uploads(self):
        return self.__uploads

    @property
    def feed(self):
        return self.__feed

    @property
    def friend(self):
        return self.__friend

    @property
    def post(self):
        return self.__post

    @property
    def user(self):
        return self.__user

    @property
    def code(self):
        return self.__code

    @property
    def chat(self):
        return self.__chat
    
    @property
    def comment(self):
        return self.__comment

    @property
    def notification(self):
        return self.__notification    

controllers = FactoryController()

