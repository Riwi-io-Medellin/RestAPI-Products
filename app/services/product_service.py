from bson import ObjectId
from app.models.product_model import ProductModel


class ProductService:
    def __init__(self, db):
        self.db = db

    def get_all_products(self):
        products = self.db.products.find()
        return [ProductModel.from_dict(product) for product in products]

    def get_product_by_id(self, id: str):
        product = self.db.products.find_one({"_id": ObjectId(id)})
        if product:
            return ProductModel.from_dict(product)
        return None

    def create_product(self, data):
        product = {
            "name": data["name"],
            "price": data["price"]
        }
        result = self.db.products.insert_one(product)
        return ProductModel.from_dict({
            "_id": result.inserted_id,
            "name": product["name"],
            "price": product["price"]
        })

    def update_product(self, id: str, data):
        # Verificar si el producto existe
        product = self.db.products.find_one({"_id": ObjectId(id)})
        if not product:
            return None

        # Actualizar el producto
        self.db.products.update_one({"_id": ObjectId(id)}, {"$set": data})

        # Devolver el producto actualizado
        updated_product = self.db.products.find_one({"_id": ObjectId(id)})
        return ProductModel.from_dict(updated_product)

    def delete_product(self, id: str):
        # Verificar si el producto existe
        product = self.db.products.find_one({"_id": ObjectId(id)})
        if not product:
            return None

        # Eliminar el producto
        self.db.products.delete_one({"_id": ObjectId(id)})
        return True