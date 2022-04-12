class User:
    def __init__(self,name,email,password,id=None) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._password = password

    def change_for_json(self):
      return {
        'id':self._id,
        'name': self._name,
        'email': self._email,
        'password': self._password
      }
        
    def __str__(self) -> str:
        return self._name

class Post:
    def __init__(self,title, description, user, create_at = None, update_at = None, like_cont = None, idPost = None, code = None) -> None:
        self._idPost = idPost
        self._title = title
        self._description = description
        self._like_cont = like_cont
        self._create_at = create_at
        self._update_at = update_at
        self._user = user
        self._code = code
        
    def set_idPost(self, idPost):
      self._idPost = idPost
class Code:
    def __init__(self, code, idPost, idUser, created_at = None) -> None:
        self._code = code
        self._idPost = idPost
        self._idUser = idUser
        self._created_at = created_at


        

  
