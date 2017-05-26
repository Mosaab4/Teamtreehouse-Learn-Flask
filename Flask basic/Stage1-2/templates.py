from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name = 'sss'):
    return "hello from {}".format(name)


@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
def add(num1,num2):
    return """
        <!doctype html>
        <html>
            <head><tilte>Adding</title></head>

            <body>
                <h1>{} + {} = {}</h1>
                </body>
        </html>
    """.format(num1,num2 ,num1+num2)


if __name__ == '__main__':
    app.run(debug = True)
