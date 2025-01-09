from flask import Blueprint, request, jsonify
from bson import ObjectId
from app import mongo

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    return jsonify([{"id": str(product["_id"]), "name": product["name"], "price": product["price"]} for product in products]), 200

@product_bp.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"id": str(product["_id"]), "name": product["name"], "price": product["price"]}), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Validación de los datos
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"error": "Nombre y precio son obligatorios"}), 400

    product = {
        "name": data["name"],
        "price": data["price"]
    }

    result = mongo.db.products.insert_one(product)
    return jsonify({"id": str(result.inserted_id), "name": product["name"], "price": product["price"]}), 201


@product_bp.route('/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()

    # Validación de los datos
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"error": "Nombre y precio son obligatorios"}), 400

    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Actualizar el producto
    mongo.db.products.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Producto actualizado con éxito"}), 200


@product_bp.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = mongo.db.products.find_one({"_id": ObjectId(id)})
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Eliminar el producto
    mongo.db.products.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Producto eliminado con éxito"}), 200
