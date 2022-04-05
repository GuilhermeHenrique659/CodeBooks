from flask import render_template,request,redirect,url_for
from config import server
from dao import PostDao

post_dao = PostDao(server.db)

class ControllerPost:
    def __init__(self) -> None:
        pass

    def list_post(self):
        return post_dao.list_post()
        
