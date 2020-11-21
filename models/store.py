from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # sql knows the store_id in the item is a single store that many items can
    # be related to i -- Lazy means that the items n the store are not actually created until the json method is
    # called, this means the store is created faster

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
