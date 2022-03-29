from config import server
from controllers.controllers import ControllerLogin

login_controllers = ControllerLogin()

class Routes:
    def __init__(self) -> None:
        server.app.add_url_rule('/',endpoint='index',view_func=login_controllers.index)
        server.app.add_url_rule('/login',endpoint='login',view_func=login_controllers.login)
        server.app.add_url_rule('/register',endpoint='register',view_func=login_controllers.register)
        server.app.add_url_rule('/authenticate',endpoint='authenticate',view_func=login_controllers.authenticate,methods=['POST'])
        server.app.add_url_rule('/sing_in',endpoint='sing_in',view_func=login_controllers.sing_in,methods=['POST'])