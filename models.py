from flask import url_for

FIRST_FILE = 0

class User:
    def __init__(self,name,email,password,id  =None, age = None, image = None, job = None) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._password = password
        self._age = age
        self._image = image
        self._job = job

    def change_for_json(self):
      return {
        'id':self._id,
        'name': self._name,
        'email': self._email,
        'password': self._password,
        'image': url_for('uploads', filename=self.image)
      }

    def set_image(self,image):
      self._image = image

    @property
    def image(self):
      if not self._image:
        self._image = 'image_not_found.jfif'
      return self._image

    @property
    def name(self):
      if not self._name:
        self._name = 'usuario não encontrado'
      return self._name

    @property
    def id(self):
      if not self._id:
        self._id = 0
      return self._id

    def __str__(self) -> str:
        return self._name

class Post:
    def __init__(self,title, description, user, create_at = None, update_at = None, like_cont = None, idPost = None, code = None, files=None) -> None:
        self._idPost = idPost
        self._title = title
        self._description = description
        self._like_cont = like_cont
        self._create_at = create_at
        self._update_at = update_at
        self._user = user
        self._code = code
        self._files = files
        
    def set_idPost(self, idPost):
      self._idPost = idPost
    
    def set_files(self, files): 
      self._files = files

    def get_first_file(self):
        first_file = self._files[FIRST_FILE]
        self._files.pop(FIRST_FILE)
        return first_file

class Code:
    def __init__(self, code, idPost, user, created_at = None, idcode = None) -> None:
        self._idcode = idcode
        self._code = code
        self._idPost = idPost
        self._user = user
        self._created_at = created_at

class File:
    def __init__(self, filename, type, id_post) -> None:
        self._filename = filename
        self._type = type
        self._id_post = id_post
    
class Comment:
    def __init__(self, Comment, idPost, idUser, idComment = None) -> None:
        self._Comment = Comment
        self._idPost = idPost
        self._idUser = idUser
        self._idComment = idComment



        

  
