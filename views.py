import jwt
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from extensions import Session
from models import User, AdvertisementModel
from schema import PatchUser, CreateUser, AuthUser, \
    AdvertisementSchema
from service import HttpError, validate_json, hash_password


class UserView(MethodView):

    @staticmethod
    def get_user(session: Session, user_id: int):
        user = session.get(User, user_id)
        if user is None:
            raise HttpError(404, "User doesn't exist")
        return user

    def get(self, user_id: int):
        with Session() as session:
            user = self.get_user(session, user_id)
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
        access_token = jwt.decode(request.headers.get('Authorization'),
                                  "secret", algorithms=["HS256"])
        if json_data.get('password'):
            json_data['password'] = hash_password(json_data['password'])
        else:
            del json_data['password']
        with Session() as session:
            user = self.get_user(session, user_id)
            if user.id == access_token.get('payload'):
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
            else:
                raise HttpError(403, f'Permission denied')

    def delete(self, user_id: int):
        with Session() as session:
            user = self.get_user(session, user_id)
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
                raise HttpError(409, f'Wrong password')


class AdvetisementView(MethodView):

    @staticmethod
    def get_adv(session: Session, adv_id: int):
        adv = session.get(AdvertisementModel, adv_id)
        if adv is None:
            raise HttpError(404, "Advertisement doesn't exist")
        return adv

    def get(self, adv_id: int):
        with Session() as session:
            adv = self.get_adv(session, adv_id)
            return jsonify({'id': adv.id,
                            'title': adv.title,
                            'text': adv.text,
                            'created_at': adv.created_at,
                            'owner': adv.owner.username})

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
                            'owner': adv.owner.username})

    def delete(self, adv_id: int):
        with Session() as session:
            adv = self.get_adv(session, adv_id)
            session.delete(adv)
            try:
                session.commit()
            except Exception as e:
                raise HttpError(500,
                                f'ERORR: {e}')
            return jsonify({'id': adv.id})
