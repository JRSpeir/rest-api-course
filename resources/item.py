import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # no delf. means method belongs to the class
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Do not leave blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occured finding the item"}, 500
        if item:
            return item.json(), 201
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):  # if item exists
            return {'message': "an item with name '{}' already exists".format(
                name)}, 400  # 400 is bad request as item already exists

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # **data = data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error has occured inserting the item"}, 500  # 500=internal server error

        return item.json(), 201  # can return item as it is JSON

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):  # if item already exists update it
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, data['price'], data['store_id'])

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
