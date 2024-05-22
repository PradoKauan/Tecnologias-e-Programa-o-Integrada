import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_products():
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
    except FileNotFoundError:
        products = []
    return products

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products = load_products()
    products.append(data)
    save_products(products)
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = load_products()
    return jsonify(products)

@app.route('/products/<int:id>/stock', methods=['PUT'])
def update_stock(id):
    data = request.json
    products = load_products()
    for product in products:
        if product['id'] == id:
            product['stock'] = data['stock']
            save_products(products)
            return jsonify({'message': 'Estoque atualizado com sucesso!'})
    return jsonify({'error': 'Produto não encontrado!'}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products = load_products()
    for product in products:
        if product['id'] == id:
            products.remove(product)
            save_products(products)
            return jsonify({'message': 'Produto excluído com sucesso!'})
    return jsonify({'error': 'Produto não encontrado!'}), 404

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    cart = load_cart()
    cart.append(data)
    save_cart(cart)
    return jsonify({'message': 'Produto adicionado ao carrinho com sucesso!'}), 201

def load_cart():
    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
    except FileNotFoundError:
        cart = []
    return cart

def save_cart(cart):
    with open('cart.json', 'w') as file:
        json.dump(cart, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
