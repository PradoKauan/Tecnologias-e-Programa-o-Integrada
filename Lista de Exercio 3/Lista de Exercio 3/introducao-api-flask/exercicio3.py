import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
    return tasks

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    tasks = load_tasks()
    tasks.append(data)
    save_tasks(tasks)
    return jsonify({'message': 'Tarefa adicionada com sucesso!'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/tasks/<int:index>/complete', methods=['PUT'])
def complete_task(index):
    tasks = load_tasks()
    if index < len(tasks):
        tasks[index]['completed'] = True
        save_tasks(tasks)
        return jsonify({'message': 'Tarefa marcada como concluída!'})
    else:
        return jsonify({'error': 'Índice de tarefa inválido!'}), 404

@app.route('/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    tasks = load_tasks()
    if index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
        return jsonify({'message': 'Tarefa excluída com sucesso!'})
    else:
        return jsonify({'error': 'Índice de tarefa inválido!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
