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

    class Meta:
        database = DATABASE 
        order_by = ('-joined_at',) #- for showing the newest members

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user == self )
        )

    def following(self):
        """the user we are following."""
        return (
            User.select().join(
                Relationship,on = Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )

    def followers(self):
        """Get users following the current user"""
        return (
            User.select().join(
                Relationship, on = Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    @classmethod #if we don't have the decorator ,we have to creat a user instance to call the function create_user
    def create_user(cls , username ,email, password , admin = False): #cls refered to user class
        try :
            with DATABASE.transaction():
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

    class Meta :
        database = DATABASE
        order_by = ('-timestamp',)

class Relationship():
    from_user = ForeignKeyField(User, related_name = 'relationship')
    to_user = ForeignKeyField(User, related_name='related_to')
    
    class Meta:
        database = DATABASE
        indexes = (
            (('from_user','to_user'), True)
        )
def initialize():
    #DATABASE.connect()
    DATABASE.get_conn()
    DATABASE.create_tables([User,Post,Relationship] , safe = True)
    DATABASE.close()