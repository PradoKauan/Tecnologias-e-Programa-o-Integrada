from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Criando a tabela Enquete
class Enquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.Text, nullable=False)
    opcoes = db.relationship('Opcao', backref='enquete', lazy=True)

# Criando a tabela Opcao
class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    votos = db.Column(db.Integer, default=0, nullable=False)
    enquete_id = db.Column(db.Integer, db.ForeignKey('enquete.id'), nullable=False)


#1.Criar Enquete - OK
@app.route('/api/enquetes', methods=['POST'])
def create_enquete():
    data = request.json
    new_enquete = Enquete(pergunta=data['pergunta'])
    db.session.add(new_enquete)
    db.session.commit()
    return jsonify({"message": "Enquete created successfully"}), 201


#2.Listar todas as Enquetes - OK
@app.route('/api/enquetes', methods=['GET'])
def consultar_enquetes():
    enquetes = Enquete.query.all()
    enquetes_list = []
    for enquete in enquetes:
        enquete_data = {
            "id": enquete.id,
            "Pergunta": enquete.pergunta
        }
        enquetes_list.append(enquete_data)
    return jsonify(enquetes_list), 200


#3. Consultar uma Enquete - OK
@app.route('/api/enquetes/<int:id>', methods=['GET'])
def consultar_enquete_por_id(id):
    enquete = Enquete.query.get(id)
    if enquete:
        return jsonify({'pergunta':enquete.pergunta})
    return jsonify({'mensagem': 'Enquete Não encontrada'}),404
    
#4. Votar em uma opção - OK
@app.route('/api/enquetes/<int:opcao_id>/votar', methods=['POST'])
def votar(opcao_id):
    opcao = Opcao.query.get_or_404(opcao_id)
    opcao.votos += 1
    db.session.commit()
    return jsonify({'mensagem': 'Voto registrado com sucesso!'}), 200

#5. Resultados de uma enquete -OK
@app.route('/api/enquetes/<int:enquete_id>/resultados', methods=['GET'])
def resultado_enquete(enquete_id):
    enquete = Enquete.query.get_or_404(enquete_id)
    opcoes = enquete.opcoes
    resultado = [{'opcao': opcao.texto, 'votos': opcao.votos} for opcao in opcoes]
    return jsonify({'enquete': enquete.pergunta, 'opcoes': resultado}), 200
    
#6. Visualizar opções de uma enquete - OK
@app.route('/api/enquetes/<int:enquete_id>/opcoes', methods=['GET'])
def opcoes_enquete(enquete_id):
    enquete = Enquete.query.get_or_404(enquete_id)
    opcoes = [{'id': opcao.id, 'texto': opcao.texto} for opcao in enquete.opcoes]
    return jsonify({'pergunta': enquete.pergunta, 'opcoes': opcoes}), 200

#7. Adicionar opção -OK
@app.route('/api/enquetes/<int:enquete_id>/opcoes', methods=['POST'])
def adicionar_opcao(enquete_id):
    dados = request.json
    enquete = Enquete.query.get_or_404(enquete_id)
    nova_opcao = Opcao(texto=dados['texto'], enquete=enquete)
    if enquete:
        db.session.add(nova_opcao)
        db.session.commit()
        return jsonify({'mensagem': 'Opção adicionada com sucesso!'}), 201
    else:
        return jsonify({'mensagem': 'Enquete não encontrada!'}), 404

#8.Deletar Enquete - OK
@app.route('/api/enquetes/<int:enquete_id>', methods=['DELETE'])
def delete_enquete(enquete_id):
    enquete = Enquete.query.get(enquete_id)
    enquete
    db.session.delete(enquete)
    db.session.commit()
    return jsonify({"message": "Enquete deletada com sucesso"}), 200
   
#9.Deletar opção - OK
@app.route('/api/enquetes/<int:enquete_id>/opcoes/<int:opcao_id>', methods=['DELETE'])
def excluir_opcao(enquete_id, opcao_id):
    pergunta = Enquete.query.get_or_404(enquete_id)
    opcao = Opcao.query.get_or_404(opcao_id)
    if opcao in pergunta.opcoes:
        db.session.delete(opcao)
        db.session.commit()
        return jsonify({'mensagem': 'Opção excluída com sucesso!'}), 200
    else:
        return jsonify({'mensagem': 'Opção não encontrada nesta pergunta.'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)