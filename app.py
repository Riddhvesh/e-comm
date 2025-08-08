from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

def seed_data():
    if Product.query.count() == 0:
        sample_products = [
            Product(title="Laptop", price=55000, image="https://via.placeholder.com/200"),
            Product(title="Smartphone", price=25000, image="https://via.placeholder.com/200"),
            Product(title="Headphones", price=2000, image="https://via.placeholder.com/200")
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "title": p.title, "price": p.price, "image": p.image} for p in products])

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    return jsonify({"message": "Product added to cart", "product": data}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
