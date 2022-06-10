from config import server

cursor = server.db.cursor()

cursor.execute(''' 
create table if not exists users (
  iduser serial primary key,
  username varchar(45) not null unique,
  name varchar(55) not null,
  email varchar(65) not null unique,
  city varchar(65) null,
  state varchar(55) null,
  bibliografy text null,
  age date not null,
  image varchar(360),
  job varchar(55),
  password varchar(128) not null
);

drop table friendship;
create table if not exists friendship (
  idfriendship serial primary key,
  user_iduser integer not null,
  friend_iduser integer not null,
  friend_confirm integer not null,
  constraint fk_user_has_user_user
    foreign key (user_iduser)
    references users (iduser)
    on delete cascade
    on update cascade,
  constraint fk_user_has_user_user1
    foreign key (friend_iduser)
    references users (iduser)
    on delete cascade
    on update cascade);

drop table notifications;
create table if not exists notifications (
    idnoti serial primary key,
    action varchar(128) not null,
    type varchar(45) not null,
    message varchar(128) null,
    iduser int null,
    constraint fk_notfi_user
      foreign key (iduser)
      references users (iduser)
      on delete cascade
      on update cascade
);

create table if not exists post (
  idpost serial primary key,
  title varchar(45) not null,
  description text not null,
  like_cont integer null,
  created_at timestamp default current_timestamp not null,
  updated_at timestamp default current_timestamp not null,
  user_iduser int null,
  constraint fk_post_user1
    foreign key (user_iduser)
    references users (iduser)
    on delete set null
    on update cascade);

create table if not exists files (
  idfile serial primary key,
  file varchar(155) not null,
  type varchar(15) not null,
  idpost int not null,
  constraint fk_files_post1
    foreign key (idpost)
    references post (idpost)
    on delete cascade
    on update cascade);


create table if not exists code (
  idcode serial primary key,
  code text not null,
  created_at timestamp default current_timestamp not null,
  post_idpost integer not null,
  user_id int null,
  constraint fk_code_post1
    foreign key (post_idpost)
    references post (idpost)
    on delete cascade
    on update cascade,
  constraint fk_code_user
    foreign key (user_id)
    references users (iduser)
    on delete set null
    on update cascade);


create table if not exists comment (
  idcomment serial primary key,
  comment text not null,
  created_at timestamp default current_timestamp not null,
  post_idpost integer not null,
  user_iduser integer not null,
  constraint fk_comment_post1
    foreign key (post_idpost)
    references post (idpost)
    on delete cascade
    on update cascade,
  constraint fk_comment_user1
    foreign key (user_iduser)
    references users (iduser)
    on delete cascade
    on update cascade);
''')

server.db.commit()