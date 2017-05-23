import json
from flask import (Flask , render_template ,
        redirect,url_for,request, make_response)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save' ,methods=['POST'])
def save():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)
