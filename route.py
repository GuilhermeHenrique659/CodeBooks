
from config import server
from controllers.systemcontrollers import ControllerLogin,ControllerRegister, ControllerUploads
from controllers.feedcontrollers import ControllerFeed
from controllers.friendcontroller import ControllerFriend
from controllers.postcontrollers import ControllerPost
from controllers.usercontrollers import ControllerUser
from models import User

login_controllers = ControllerLogin()
register_controller = ControllerRegister()
feed_controller = ControllerFeed()
friend_controller = ControllerFriend()
post_controller = ControllerPost()
user_controller = ControllerUser()
uploads_controller = ControllerUploads()

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

        server.app.add_url_rule('/create_post', endpoint='create_post', view_func=post_controller.create_post,methods = ['POST'])

        server.app.add_url_rule('/user_profile', endpoint='user_profile', view_func= user_controller.user_profile )

        server.app.add_url_rule('/user_edit_save', endpoint='user_save',view_func=user_controller.user_edit_save,methods = ['POST'])

        server.app.add_url_rule('/uploads/<filename>',endpoint='uploads',view_func=uploads_controller.upload_folder)