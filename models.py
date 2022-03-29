class User:
    def __init__(self,name,email,password,id=None) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._password = password
        