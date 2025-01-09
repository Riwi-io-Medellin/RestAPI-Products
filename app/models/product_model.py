class ProductModel:
    def __init__(self, id: str, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @classmethod
    def from_dict(cls, data):
        return cls(id=str(data["_id"]), name=data["name"], price=data["price"])

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

