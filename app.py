from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, Stores


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'jose'
api = Api(app)


# @app.before_request
# def create_tables():
#     db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Item, '/iterm/<string:name>')
api.add_resource(ItemList, '/iterms')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
