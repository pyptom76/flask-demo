from flask_restful import Resource, reqparse
from blocklist import BLOCKLIST
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt
)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and compare_digest(user.u_pass, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def delete(cls):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'successfully logged out'}, 200
