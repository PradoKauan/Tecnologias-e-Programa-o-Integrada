from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = [
    {
        'ID': 1,
        'Nome': 'Kauan',
        'Sorenome': 'Prado',
    },
    {
        'ID': 2,
        'Nome': 'Joao',
        'Sorenome': 'Silva',
    },
    {
        'ID': 3,
        'Nome': 'Paulo',
        'Sorenome': 'Marques',
    }
]

#Consultar todos os usuários
@app.route('/usuarios', methods=['GET'])
def consultar_todos():
    return jsonify(usuarios)

        
#Consultar por Nome
@app.route('/usuarios/consultaNome/<string:Nome>', methods=['GET'])
def consultar_usuario_nome(Nome):
    for nome in usuarios:
        if nome.get("Nome") == Nome:
            return jsonify(nome)
        
#Consultar por ID
@app.route('/usuarios/consultaID/<int:ID>', methods=['GET'])
def consultar_usuario_id(ID):
    for nome in usuarios:
        if nome.get("ID") == ID:
            return jsonify(nome)

#Alterar usuario
@app.route('/usuarios/altera/<int:ID>', methods=['PUT'])
def editar_usuario_id(ID):
    usuario_alterado = request.get_json()
    for indice, nome in enumerate(usuarios):
        if nome.get('ID') == ID:
            usuarios[indice].update(usuario_alterado)
            return jsonify(usuarios[indice])

#Criar usuario
@app.route('/usuarios/criar', methods=['POST'])
def criar_usuario():
    novo_usuario = request.get_json()
    usuarios.append(novo_usuario)
    return jsonify(usuarios)

#Excluir usuario
@app.route('/usuarios/excluir/<int:ID>', methods=['DELETE'])
def excluir_usuario (ID):
    for i, nome in enumerate(usuarios):
        if nome.get('ID') == ID:
            del usuarios[i]
    return jsonify(usuarios)


app.run(port=5000,host='localhost',debug=True)