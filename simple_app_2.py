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
    return str(num1+num2)
    #return "{} + {} = {}".format(num1,num2 , int(num1)+int(num2))
    return "{} + {} = {}".format(num1,num2 ,num1+num2)

@app.route('/multiply/<int:num1>/<int:num2>')
@app.route('/multiply/<float:num1>/float:num2>')
@app.route('/multiply/<int:num1>/<float:num2>')
@app.route('/multiply/<float:num1>/<int:num2>')
def multiply(num1,num2):
    return str(num1*num2)
    return "{} + {} = {}".format(num1,num2 ,num1*num2)
    
if __name__ ='__main__':
    app.run(debug = True)
