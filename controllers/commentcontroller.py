from click import command
from config import server
from flask import redirect, render_template, session,request, url_for
from factoryDao import dao
from models import Comment

class ControllerComment:
    @server.loggin_required
    def insertComment(self):
        dataComment = request.form
        dataIdPost = request.args['idPost']
        comment = Comment(dataComment['comment'], dataIdPost, session['user_id'])
        dao.comment.save_comment(comment)
        return redirect(url_for('post', id=dataIdPost))
        
        
        