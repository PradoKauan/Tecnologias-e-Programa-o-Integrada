from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



# Criar Enquete
class Enquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pergunta = db.Column(db.Text, nullable=False)
   
#Deletar Enquete
@app.route('/api/enquetes/delete/<int:enquete_id>', methods=['DELETE'])
def delete_enquete(enquete_id):
    enquete = Enquete.query.get(enquete_id)
    if enquete:
        db.session.delete(enquete)
        db.session.commit()
        return jsonify({"message": "Enquete deleted successfully"}), 200
    else:
        return jsonify({"message": "Enquete not found"}), 404
   
#Listar Enquetes
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

@app.route('/api/enquete/id/<int:enquete_id>', methods=['GET'])
def consultar_enquete(id):
    for id in Enquete:
        if id.get("id") == id:
            return jsonify(id)
   

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)