import json

import bcrypt
from flask import Flask, jsonify, request
from flask_jwt import JWTError
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from src import google_auth
from src.models.user import UserModel
from src.resources.user import UserRegister
from src.google_auth import logout
from src.facebook_oauth import facebook_login, facebook_callback
from src.google_auth import google_auth_redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Masaki2017$$@localhost/okoafarmer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = '#^#%^%&#BgdvttkkgyDDT&*%$'  # to encode cookies
api = Api(app)

jwt = JWTManager(app)


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


# Route
# api.add_resource(UserRegister, '/register/<string:name>')
api.add_resource(UserRegister, '/register')


@app.route("/")
def index():
    return """
    <a href="/fb-login">Login with Facebook</a>
    <a href="/google/login">Login with Google</a>
    """


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return 'Missing Username', 400
        if not password:
            return 'Missing password', 400

        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return 'User Not Found!', 404

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity={"username": username})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide a Username and Password in JSON format in the request body', 400


# app.register_blueprint(google_auth.app)
@app.route('/google/login')
def google_login():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return jsonify({'user_info': json.dumps(user_info, indent=4), 'message': 'You have logged in successfully'})

    return jsonify({'message': 'You are not currently logged in.'})


@app.route('/google/auth')
def goog_redirect():
    google_auth_redirect()


@app.route('/google/logout')
def signOutUser():
    if google_auth.is_logged_in():
        logout()
    return jsonify({'message': 'You are not currently logged in.'})


# facebook routes
@app.route("/fb-login")
def fb_login():
    facebook_login()


@app.route("/fb-callback")
def callback():
    print('apa nayoo nafika')
    facebook_callback()


@app.route("/kujuana",methods=['GET'])
@jwt_required
def testing_things():
    return "The beaty of it all"


if __name__ == "__main__":
    from src.models.Model import db

    db.init_app(app)

    app.run(host='0.0.0.0', port=4000, debug=True)
