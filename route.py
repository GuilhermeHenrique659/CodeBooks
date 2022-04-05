from config import server
from controllers.systemcontrollers import ControllerLogin,ControllerRegister
from controllers.feedcontrollers import ControllerFeed
from controllers.friendcontroller import ControllerFriend

login_controllers = ControllerLogin()
register_controller = ControllerRegister()
feed_controller = ControllerFeed()
friend_controller = ControllerFriend()

class Routes:
    def __init__(self) -> None:
        server.app.add_url_rule('/',endpoint='index',view_func=feed_controller.index)

        server.app.add_url_rule('/login',endpoint='login',view_func=login_controllers.login)

        server.app.add_url_rule('/register',endpoint='register',view_func=register_controller.register)

        server.app.add_url_rule('/authenticate',endpoint='authenticate',view_func=login_controllers.authenticate,methods=['POST'])

        server.app.add_url_rule('/sing_in',endpoint='sing_in',view_func=register_controller.sing_in,methods=['POST'])

        server.app.add_url_rule('/logout', endpoint='logout',view_func=login_controllers.logout)

        server.app.add_url_rule('/search_user', endpoint='search_user', view_func=friend_controller.seach_user, methods=['POST','GET'])

        server.app.add_url_rule('/add_friend/<int:id>',endpoint='add_friend',view_func=friend_controller.add_friend, methods=['GET'])