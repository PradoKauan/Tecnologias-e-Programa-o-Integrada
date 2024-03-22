from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Criando a tabela Enquete
class Enquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.Text, nullable=False)
   

#1.Criar Enquete
@app.route('/api/enquetes', methods=['POST'])
def create_enquete():
    data = request.get_json()
    new_enquete = Enquete(pergunta=data['pergunta'])
    db.session.add(new_enquete)
    db.session.commit()
    return jsonify({"message": "Enquete created successfully"}), 201


#2.Listar todas as Enquetes
@app.route('/api/enquetes', methods=['GET'])
def consultar_enquetes():
    enquetes = Enquete.query.all()
    enquetes_list = []
    for enquete in enquetes:
        enquete_data = {
            "id": enquete.id,
            "content": enquete.pergunta
        }
        enquetes_list.append(enquete_data)
    return jsonify(enquetes_list), 200


#3. Consultar uma Enquete
@app.route('/api/enquetes/<int:id>', methods=['GET'])
def consultar_enquete_por_id(id):
    enquete = Enquete.query.get(id)
    if enquete:
        return jsonify({'pergunta':enquete.pergunta})
    return jsonify({'mensagem': 'Enquete Não encontrada'}),404
    

#8.Deletar Enquete
@app.route('/api/enquetes/<int:enquete_id>', methods=['DELETE'])
def delete_enquete(enquete_id):
    enquete = Enquete.query.get(enquete_id)
    if enquete:
        db.session.delete(enquete)
        db.session.commit()
        return jsonify({"message": "Enquete deleted successfully"}), 200
    else:
        return jsonify({"message": "Enquete not found"}), 404
   


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)