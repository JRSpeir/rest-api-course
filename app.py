# MUST run from top level folder e.g. code/app.py otherwise won'#t be able to find db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # you can use postgres or my sql by changing this line here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


app.secret_key = 'jose'

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/name

api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
