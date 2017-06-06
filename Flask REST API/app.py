from flask import Flask

import models

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'





if __name__ == '__main__':
    models.initialize()
    app.run(debug = True)