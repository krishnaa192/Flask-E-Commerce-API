from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy class from flask_sqlalchemy module to create a database

app = Flask(__name__)

#Add sqlite database path to app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
db = SQLAlchemy(app)


#Create a Product model
class Product(db.Model):
    #Create a table with the name products
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(120))
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(120))

# Create a method to return a JSON representation of the model
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url
        }

#Create a CartItem model
class CartItem(db.Model):
    #Create a table with the name cart_items
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
#Create the database and update the tables
with app.app_context():
    db.create_all()
  

#Create a route to get products
@app.route('/products', methods=['GET'])
def get_products():
    try:
        #Query the database to get all products
        products = Product.query.all()
        return jsonify([product.json() for product in products]), 200
    except:
        return jsonify({'message': 'No products to show'}), 404

#Create a route to get specific product
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify(product.json()), 200
    except:
        return jsonify({'message': 'Product not found'}), 404

#Create a route to add cart
@app.route('/cart', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 200
    try:
        return jsonify([cart_item.json() for cart_item in cart_items]), 200
    except:
        return jsonify({'message': 'Error'}), 404

#Create a route to create a cartItem
@app.route('/cart', methods=['POST'])
def add_to_cart():
    #check if product exists
    product_id = request.json.get('product_id')
    if not Product.query.get(product_id):
        return jsonify({'message': 'Product not found'}), 404
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


#Create a route to remove a cartItem
@app.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):
    try:
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart successfully'}), 200
    except:
        return jsonify({'message': 'Failed to remove product from cart'}), 404

#run the app
if __name__ == '__main__':
    app.run(debug=True)
