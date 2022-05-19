from config import server

cursor = server.db.cursor()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS users (
  idUser serial PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  email VARCHAR(65) NOT NULL UNIQUE,
  age DATE NOT NULL,
  image VARCHAR(360),
  job VARCHAR(55),
  password VARCHAR(128) NOT NULL
);


CREATE TABLE IF NOT EXISTS Friendship (
  User_idUser INTEGER NOT NULL,
  Friend_idUser INTEGER NOT NULL,
  PRIMARY KEY (User_idUser, Friend_idUser),
  CONSTRAINT fk_User_has_User_User
    FOREIGN KEY (User_idUser)
    REFERENCES users (idUser)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_User_has_User_User1
    FOREIGN KEY (Friend_idUser)
    REFERENCES users (idUser)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS Post (
  idPost serial PRIMARY KEY,
  title VARCHAR(45) NOT NULL,
  description TEXT NOT NULL,
  like_cont INTEGER NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  User_idUser INT NULL,
  CONSTRAINT fk_Post_User1
    FOREIGN KEY (User_idUser)
    REFERENCES users (idUser)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS Files (
  idFile serial PRIMARY KEY,
  file VARCHAR(155) NOT NULL,
  type VARCHAR(15) NOT NULL,
  idPost INT NOT NULL,
  CONSTRAINT fk_Files_Post1
    FOREIGN KEY (idPost)
    REFERENCES Post (idPost)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


CREATE TABLE IF NOT EXISTS Code (
  idCode serial PRIMARY KEY,
  code TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Post_idPost INTEGER NOT NULL,
<<<<<<< HEAD
  User_id INT NOT NULL,
=======
  User_id INT NULL,
>>>>>>> c91d82bc19daa05441344e0fe7435a317f4a5369
  CONSTRAINT fk_Code_Post1
    FOREIGN KEY (Post_idPost)
    REFERENCES Post (idPost)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Code_User
    FOREIGN KEY (User_id)
    REFERENCES users (idUser)
    ON DELETE SET NULL
    ON UPDATE CASCADE);


CREATE TABLE IF NOT EXISTS Comment (
  idComment serial PRIMARY KEY,
  Comment TEXT NOT NULL,
  like_cont INTEGER NULL,
  Post_idPost INTEGER NOT NULL,
  User_idUser INTEGER NOT NULL,
  CONSTRAINT fk_Comment_Post1
    FOREIGN KEY (Post_idPost)
    REFERENCES Post (idPost)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Comment_User1
    FOREIGN KEY (User_idUser)
    REFERENCES users (idUser)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
''')