from sqlalchemy import Column,String,Integer,ForeignKey,TIMESTAMP
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class rooms(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    numOfUsers = Column(Integer)
    doorState = Column(Integer,nullable=False)
    maxNumOfUsers = Column(Integer,default=10)
    roomNumber = Column(Integer,nullable=False,unique=True)

class users(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    userName = Column(String(20),nullable=False)
    password = Column(String(255),nullable=False)
    keyPasswd = Column(Integer,unique=True)
    tokenVersion = Column(Integer)
    roomNumber = Column(Integer,ForeignKey('rooms.roomNumber'))

class boards(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    codes = Column(String(255),unique=True,nullable=False)