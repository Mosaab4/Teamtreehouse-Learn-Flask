import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('social.db')

class User(UserMixin , Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField(max_length = 100)
    joined_at = DateTimeField(default = datetime.datetime.now ) #now not now() to make the time when the model creatd not the time of running the program
    is_admin = BooleanField(default = False)

    class Mete:
        database = DATABASE 
        order_by = ('-joined_at',) #- for showing the newest members

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user == self )
        )

    @classmethod #if we don't have the decorator ,we have to creat a user instance to call the function create_user
    def create_user(cls , username ,email, password , admin = False): #cls refered to user class
        try :
            cls.create(#cls refered to user.create
                username = username ,
                email = email ,
                password =generate_password_hash(password),
                is_admin = admin
            )
        except IntegrityError:
                raise ValueError("user allready exists")

class Post(Model):
    timestamp = DateTimeField(default = datetime.datetime.now)
    user = ForeignKeyField(
        rel_model = User,
        related_name = 'posts' #rel name is what the rel model call this model
    )
    content = TextField()

    class Mete :
        database = DATABASE
        order_by = ('-timestamp',)

def initialize():
    #DATABASE.connect()
    DATABASE.get_conn()
    DATABASE.create_tables([User,Post] , safe = True)
    DATABASE.close()