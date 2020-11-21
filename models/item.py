from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    #  Foreign key links items together as they all belong to the same store One to Many
    #  "Foreign" is due to having a value that is identical to the Primary key of another table
    store = db.relationship('StoreModel')  # sqlalchemy knows that store is related to store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    # This stays class method as it returns an item object
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # Query comes directly from the sqlalchemy model we inherit
        # Equivalent to "SELECT * FROM items WHERE name=name LIMIT 1" (returns 1st row only)
        # Returns an ItemModel object

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()  # Can add more than one model and commit
        # This can do both insert and update!

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
