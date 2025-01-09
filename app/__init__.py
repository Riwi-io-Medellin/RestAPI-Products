from flask import Flask, jsonify
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object('app.config')

    # Inicializar MongoDB
    mongo.init_app(app)

    # Registrar rutas
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix='/api')

    # Manejo de errores globales
    @app.errorhandler(Exception)
    def handle_error(error):
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    return app
