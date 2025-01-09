from flask import jsonify

def validate_product_data(data):
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"error": "El nombre y el precio son obligatorios"}), 400
    if not isinstance(data['price'], (int, float)):
        return jsonify({"error": "El precio debe ser un número"}), 400
    return None
