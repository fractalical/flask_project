import jwt
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from extensions import Session
from models import User, AdvertisementModel
from schema import PatchUser, CreateUser, AuthUser, \
    AdvertisementSchema
from service import HttpError, validate_json, hash_password


def get_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, "User doesn't exist")
    return user


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify({'id': user.id,
                            'username': user.username,
                            'created_at': user.created_at})

    def post(self):
        json_data = validate_json(request.json, CreateUser)
        json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = User(**json_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409,
                                f'User {json_data["username"]} already exist')
            return jsonify({'id': user.id})

    def patch(self, user_id: int):
        json_data = validate_json(request.json, PatchUser)
        if json_data.get('password'):
            json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409,
                                f'User {json_data["username"]} already exist')
            return jsonify({'id': user.id,
                            'username': user.username,
                            'created_at': user.created_at})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()


class UserAuthView(MethodView):

    def post(self):
        json_data = validate_json(request.json, AuthUser)
        json_data['password'] = hash_password(json_data['password'])

        with Session() as session:
            user = session.query(User).filter(User.username == json_data.get('username')).first()
            if user.password == json_data.get('password'):
                encoded_jwt = jwt.encode({'payload': user.id}, 'secret',  algorithm="HS256")
                return jsonify({'access_token': encoded_jwt})
            else:
                raise HttpError(409,
                                f'Wrong password')


class AdvetisementView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = get_user(session, adv_id)
            return jsonify({'id': adv.id,
                            'title': adv.title,
                            'text': adv.text,
                            'created_at': adv.created_at,
                            'owner': adv.owner})

    def post(self):
        json_data = validate_json(request.json, AdvertisementSchema)
        access_token = jwt.decode(request.headers.get('Authorization'),
                                  "secret", algorithms=["HS256"])
        json_data['owner_id'] = access_token.get('payload')
        with Session() as session:
            adv = AdvertisementModel(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409,
                                f'Advertisement does not created')
            return jsonify({'id': adv.id,
                            'title': adv.title,
                            'text': adv.text,
                            'created_at': adv.created_at,
                            'owner': adv.owner})

    def patch(self, user_id: int):
        json_data = validate_json(request.json, PatchUser)
        if json_data.get('password'):
            json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409,
                                f'User {json_data["username"]} already exist')
            return jsonify({'id': user.id,
                            'username': user.username,
                            'created_at': user.created_at})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
