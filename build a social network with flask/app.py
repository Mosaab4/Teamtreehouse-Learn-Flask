from flask import (Flask ,g ,render_template , flash ,
                    redirect ,url_for)
from flask_bcrypt import check_password_hash
from flask_login import LoginManager , login_user , logout_user,login_required,current_user

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'FAAds#fXCZXC-##$!@CLZXC.ZXC,XC22skdasds'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -----------------------------------------------------------------

@login_manager.user_loader
def load_user(userid):
    try :
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist: #error from peewee 
        return None

# -----------------------------------------------------------------

@app.before_request
def before_request():
    """connect database before eache request""" 
    g.db = models.DATABASE
    #g.db.connect()
    g.db.get_conn()
    g.user = current_user


@app.after_request
def after_request(response):
    """close the database connection"""
    g.db.close()
    return response
    
# -----------------------------------------------------------------


@app.route('/register' , methods = ['GET','POST'])
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        flash("Yay , you registeres","success")

        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )

        return redirect(url_for('index'))


    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET','POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        try :
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match" , "error")
        else:
            if check_password_hash(user.password ,form.password.data):
                login_user(user) #create a cookie with the information
                flash("You'v been loged in","success")

                return redirect(url_for('index'))
            else :
                flash("Your email or password doesn't match" , "error")
    
    return render_template('login.html' , form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user() #delete the cookie created by login_user(user) 
    flash("You have been loged out ! come back soon!","success")
    return redirect(url_for('index'))

@app.route('/new_post', methods = ['GET','POST'])
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user = g.user._get_current_object(),
        content = form.content.data.strip())
        flash("Message Posted Thanks!","sucess")
        return redirect(url_for('index'))

    return render_template('post.html' , form=form)



@app.route('/')
def index():
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream = stream)

@app.route('/stream')
@app.route('/stram/<username>')
def stream(username = None):
    template = 'stream.html'

    if username and username != current_user.username:
        user = models.User.select().where(models.User.username**username).get() # ** compatison without caring about cases , look S3V4
        stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user

    if username :
        template = 'user_stream.html'

    return render_template(template , stream = stream , user = user)

@app.route('/follow/<username>')
@login_required
def follow(username):
    try :
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        pass
    else:
        try :
            models.Relationship.create(
                from_user = g.user._get_current_object(),
                to_user = to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash("You are now following {}!".format(to_user.username),"success")

if __name__ == '__main__':
    models.initialize()
    try : 
        models.User.create_user(
            username = 'mosaab',
            email = 'masaos@csmas.com',
            password = 'password',
            admin = True 
        )
    except ValueError :
        pass
    app.run(debug=True)