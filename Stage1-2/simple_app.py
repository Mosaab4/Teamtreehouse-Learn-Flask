from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name = 'sss'):
    name = request.args.get('name', name)
    return "hello from {}".format(name)



app.run(debug = True)
