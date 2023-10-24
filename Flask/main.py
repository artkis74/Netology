import pydantic
from hashlib import md5
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager

from db import Session
from models import Ads, User
from schema import CreateUser, PatchUser, CreateAds

app = Flask('app')


def validate(input_data: dict, validation_model):
    try:
        model_item = validation_model(**input_data)
        return model_item.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


class HttpError(Exception):

    def __init__(self, status_code: int, description: str | dict | list):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'description': error.description})
    response.status_code = error.status_code
    return response


def get_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def get_ad(ads_id: int, session: Session):
    ad = session.get(Ads, ads_id)
    if ad is None:
        raise HttpError(404, 'ads not found')
    return ad


def hash_password(password: str) -> str:
    return md5(password.encode()).hexdigest()


class AdsView(MethodView):

    def get(self, ads_id: int):
        with Session() as session:
            ad = get_ad(ads_id, session)
            return jsonify({'id': ad.ads_id, 'title': ad.title, 'description': ad.description,
                            'created_at': ad.created_at.isoformat(), 'owner': ad.owner})

    def post(self):
        # json_data = validate(request.json, CreateAds)
        json_data = request.json
        ads = Ads(**json_data)
        with Session() as session:
            session.add(ads)
            session.commit()
            return {'id': ads.ads_id}

    def patch(self, ads_id: int):
        json_data = validate(request.json, CreateAds)
        with Session() as session:
            ads = get_ad(ads_id, session)
            for field, value in json_data.items():
                setattr(ads, field, value)
            session.add(ads)
            session.commit()
            return jsonify({'status': 'ad is patched'})

    def delete(self, ads_id: int):
        with Session() as session:
            ad = get_ad(ads_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({'status': 'ad is deleted'})


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({'id': user.user_id, 'email': user.email,
                            'registration_at': user.registered_at.isoformat()})

    def post(self):
        json_data = request.json
        json_data = validate(json_data, CreateUser)
        json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = User(**json_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'user already exists')
            return jsonify({'id': user.user_id})

    def patch(self, user_id: int):
        json_data = validate(request.json, PatchUser)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({'status': 'patched'})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'deleted'})


app.add_url_rule('/ads/<int:ads_id>/', view_func=AdsView.as_view('ads'), methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/ads/', view_func=AdsView.as_view('create_ads'), methods=['POST'])
app.add_url_rule('/user/<int:user_id>/', view_func=UserView.as_view('user'), methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/user/', view_func=UserView.as_view('create_user'), methods=['POST'])

if __name__ == "__main__":
    app.run()
