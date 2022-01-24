DROP DATABASE hkk;
CREATE DATABASE hkk;
use hkk;

CREATE TABLE users (
user_id int primary key auto_increment,
name varchar(20) not null,
uid varchar(16) not null,
UNIQUE(uid,name)
);

CREATE TABLE attendances(
user_id int not null,
attendance_date date not null,
FOREIGN KEY (user_id)
REFERENCES users (user_id),
UNIQUE(user_id,attendance_date)
);
