from flask import Flask, request, jsonify, send_file


app = Flask(__name__)

@app.route('/')
def index():
    return 'Exercicio da calculadora!'

@app.route('/api/calculadora', methods=['GET'])
def calculadora():
    n1 = request.args.get('n1')
    n2 = request.args.get('n2')
    operador = request.args.get('operador')
    result = 0
    if operador == "+":
        result = int(n1)+int(n2)
    elif operador == "-":
        result = int(n1)-int(n2)
    elif operador == "*":
        result = int(n1)*int(n2)
    elif operador == "/":
        result = int(n1)/int(n2)
    
    mensagem = {"mensagem":f"O resultado dos valores é {result}"}

    return jsonify(mensagem), 200, {'Content-Type': 'application/json; charset=utf-8'}


