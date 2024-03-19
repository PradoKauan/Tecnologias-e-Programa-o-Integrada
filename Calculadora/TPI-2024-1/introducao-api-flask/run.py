from flask import Flask, request, jsonify, send_file
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bem-vindo à sua API simples com Flask!'


#CALCULADORA
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


#Cadastros
@app.route('/api/parametro', methods=['GET'])
def exemplo_parametro():
    nome = request.args.get('nome', 'Visitante')
    dados = {'mensagem': f'Olá, {nome}!'}
    return jsonify(dados), 200

@app.route('/api/qrcode', methods=['GET'])
def gerar_qrcode():
    conteudo = request.args.get('nome')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    temp_file_path = "temp_qrcode.png"
    img.save(temp_file_path)
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

@app.route('/api/payload', methods=['POST'])
def receber_payload():
    try:
        payload = request.get_json()
        return jsonify({"mensagem": "Payload recebido com sucesso", "payload": payload}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
