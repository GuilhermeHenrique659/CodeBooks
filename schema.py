from config import server

cursor = server.db.cursor()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS `User` (
  `idUser` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(65) NOT NULL,
  `age` DATE NOT NULL,
  `password` VARCHAR(128) NOT NULL
)


CREATE TABLE IF NOT EXISTS `Friendship` (
  `User_idUser` INTEGER NOT NULL,
  `Friend_idUser` INTEGER NOT NULL,
  PRIMARY KEY (`User_idUser`, `Friend_idUser`),
  CONSTRAINT `fk_User_has_User_User`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_User_has_User_User1`
    FOREIGN KEY (`Friend_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS `CodeBooksDB`.`Post` (
=======
CREATE TABLE IF NOT EXISTS `Post` (
>>>>>>> bfac567bf5eae9248b39eff22783a62b35c5ca5d
  `idPost` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `like_cont` INTEGER NULL,
  `created_at` TIMESTAMP NOT NULL,
  `updated_at` TIMESTAMP NULL,
  `User_idUser` INT NOT NULL,
  CONSTRAINT `fk_Post_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS `CodeBooksDB`.`Code` (
  `idtable1` INTEGER PRIMARY KEY AUTOINCREMENT,
  `code` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `Post_idPost` INTEGER NOT NULL,
=======
CREATE TABLE IF NOT EXISTS `Code` (
  `idCode` INTEGER PRIMARY KEY AUTOINCREMENT,
  `code` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `Post_idPost` INTEGER NOT NULL,
  `User_id` INTERGER NOT NULL,
>>>>>>> bfac567bf5eae9248b39eff22783a62b35c5ca5d
  CONSTRAINT `fk_Code_Post1`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE CASCADE
<<<<<<< HEAD
    ON UPDATE CASCADE)


CREATE TABLE IF NOT EXISTS `CodeBooksDB`.`Comment` (
=======
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Code_User`
    FOREIGN KEY (`User_id`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    )


CREATE TABLE IF NOT EXISTS `Comment` (
>>>>>>> bfac567bf5eae9248b39eff22783a62b35c5ca5d
  `idComment` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Comment` TEXT NOT NULL,
  `like_cont` INTEGER NULL,
  `Post_idPost` INTEGER NOT NULL,
  `User_idUser` INTEGER NOT NULL,
  CONSTRAINT `fk_Comment_Post1`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Comment_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
<<<<<<< HEAD

=======
>>>>>>> bfac567bf5eae9248b39eff22783a62b35c5ca5d
''')