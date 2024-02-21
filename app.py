from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(120))

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

with app.app_context():
    db.create_all()
  
@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.json() for product in products]), 200
    except:
        return jsonify({'message': 'No products to show'}), 404

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify(product.json()), 200
    except:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/cart', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 200
    try:
        return jsonify([cart_item.json() for cart_item in cart_items]), 200
    except:
        return jsonify({'message': 'Error'}), 404

@app.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        cart_item = CartItem(product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product added to cart successfully'}), 201
    except:
        return jsonify({'message': 'Failed to add cart'}), 404

@app.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):
    try:
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart successfully'}), 200
    except:
        return jsonify({'message': 'Failed to remove product from cart'}), 404

if __name__ == '__main__':
    app.run(debug=True)
