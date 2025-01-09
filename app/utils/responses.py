from flask import jsonify


def success_response(data, message="Operación exitosa", status_code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status_code

def error_response(message, status_code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code
