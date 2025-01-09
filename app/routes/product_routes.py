from flask import Blueprint, request, jsonify
from bson import ObjectId
from app import mongo
from app.services.product_service import ProductService
from app.utils.responses import success_response
from app.utils.validators import validate_product_data

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    product_service = ProductService(mongo.db)
    products = product_service.get_all_products()
    return jsonify([product.to_dict() for product in products]), 200


@product_bp.route('/products/<id>', methods=['GET'])
def get_product(id):
    product_service = ProductService(mongo.db)
    product = product_service.get_product_by_id(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    product_service = ProductService(mongo.db)

    # Validación de los datos
    validation_error = validate_product_data(data)
    if validation_error:
        return validation_error

    product = product_service.create_product(data)

    return success_response({
        "id": str(product.id),
        "name": product.name,
        "price": product.price
    }, message="Producto creado con éxito", status_code=201)



@product_bp.route('/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product_service = ProductService(mongo.db)

    # Validación de los datos
    validation_error = validate_product_data(data)
    if validation_error:
        return validation_error

    # Actualizar el producto
    updated_product = product_service.update_product(id, data)

    if not updated_product:
        return jsonify({"error": "Producto no encontrado"}), 404

    return success_response({
        "id": str(updated_product.id),
        "name": updated_product.name,
        "price": updated_product.price
    }, message="Producto actualizado con éxito", status_code=200)


@product_bp.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product_service = ProductService(mongo.db)

    # Eliminar el producto
    product_deleted = product_service.delete_product(id)

    if not product_deleted:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"message": "Producto eliminado con éxito"}), 200
