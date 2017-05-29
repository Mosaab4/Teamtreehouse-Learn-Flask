import datetime

from flask_bcrypt import generate_password_hash,
from flask_login import UserMixin
from peewee import *


DATABASE SqliteDatabase('social.db')

class User(UserMixin , Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField(max_length = 100)
    joined_at = DataTimeField(default = datetime.datetime.now ) #now not now() to make the time when the model creatd not the time of running the program
    is_admin = BooleanField(default = False)

    class Mete:
        database = DATABASE 
        order_by = ('-joined_at',) #- for showing the newest members


    @classmethod
    def create_user(cls , username ,email, password , admin = False):
        try :
            cls.create(
                username = username ,
                email = email ,
                password =generate_password_hash(password),
                is_admin = admin
            )
            except IntegrityError:
                raise ValueError("user allready exists")

