import datetime

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



