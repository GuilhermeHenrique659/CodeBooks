from config import server
from controllers.factoryController import controllers

class Routes:
    def __init__(self) -> None:

        server.app.add_url_rule('/',endpoint='index',
                                    view_func=controllers.feed.index)

        server.app.add_url_rule('/login',endpoint='login',
                                    view_func=controllers.login.login)

        server.app.add_url_rule('/register',endpoint='register',
                                    view_func=controllers.register.register)

        server.app.add_url_rule('/authenticate',endpoint='authenticate',
                                    view_func=controllers.login.authenticate,methods=['POST'])

        server.app.add_url_rule('/sing_in',endpoint='sing_in',
                                    view_func=controllers.register.sing_in,methods=['POST'])

        server.app.add_url_rule('/logout', endpoint='logout',
                                    view_func=controllers.login.logout)

        server.app.add_url_rule('/search_user', endpoint='search_user', 
                                    view_func=controllers.friend.seach_user, methods=['POST','GET'])

        server.app.add_url_rule('/add_friend/<int:id>',endpoint='add_friend',
                                    view_func= controllers.friend.add_friend, methods=['GET'])

        server.app.add_url_rule('/remove_friend/<int:id>', endpoint='remove_friend',
                                    view_func= controllers.friend.remove_friend)

        server.app.add_url_rule('/create_post', endpoint='create_post', 
                                    view_func= controllers.post.create_post,methods = ['POST'])

        server.app.add_url_rule('/user_profile/<int:id>',endpoint='user_profile', 
                                    view_func =  controllers.user.user_profile)

        server.app.add_url_rule('/user_edit_save', endpoint='user_save',
                                    view_func = controllers.user.user_edit_save,methods = ['POST'])

        server.app.add_url_rule('/uploads/<filename>',endpoint='uploads',
                                    view_func =  controllers.uploads.upload_folder)

        server.app.add_url_rule('/post/<int:id>', endpoint='post', 
                                    view_func =  controllers.code.code_list,methods = ['GET']  )

        server.app.add_url_rule('/add_code/<int:id>', endpoint='add_code', 
                                    view_func =  controllers.code.add_code,methods=['POST'])

        server.app.add_url_rule('/delete_code/<int:id>', endpoint='delete_code', 
                                    view_func = controllers.code.delete_code)

        server.app.add_url_rule('/delete_account/<int:id>',endpoint='delete_account',
                    view_func=controllers.user.delete_account)
        
        server.app.add_url_rule('/chat/<int:id>', endpoint='chat', 
                                    view_func=controllers.chat.chat)

        server.app.add_url_rule('/delte_post/<int:id>', endpoint='delete_post',
                                    view_func=controllers.post.delete_post)

        server.app.add_url_rule('/edit_post', endpoint='edit_post', 
                                    view_func=controllers.post.edit_post, methods=['POST'])
        
        server.app.add_url_rule('/chat/<int:id>', endpoint='chat', view_func=controllers.chat.chat)
        
        server.app.add_url_rule('/insert_comment', endpoint='insert_comment', view_func=controllers.comment.insertComment, methods=['POST'])