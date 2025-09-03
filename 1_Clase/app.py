from flask import Flask

app = Flask(__name__)

@app.route('/opc0')
def home1():
    return 'Hola, esta es la opcion 0'

@app.route('/opc1')
def home2():
    return 'Hola, esta es la opcion 1'

@app.route('/opc2')
def home3():
    return 'Hola, esta es la opcion 2'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
