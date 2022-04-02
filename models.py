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