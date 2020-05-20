from datetime import datetime

from flask import Flask, jsonify, Blueprint, request, make_response
from flask_restful import Api
from flask_jwt import JWT, JWTError
from werkzeug.security import check_password_hash

from src import google_auth
import json
from security import authenticate, identity
from src.models.user import UserModel
from src.resources.user import UserRegister
from src.google_auth import logout
from src.facebook_oauth import facebook_login, facebook_callback
from src.google_auth import google_auth_redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Masaki2017$$@localhost/okoafarmer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '#^#%^%&#BgdvttkkgyDDT&*%$'# to encode cookies
api = Api(app)
# api_bp = Blueprint('api', __name__)
# api = Api(api_bp)
# app.register_blueprint(google_auth.app)

jwt = JWT(app, authenticate, identity)  # /auth


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


# Route
api.add_resource(UserRegister, '/register')


@app.route("/")
def index():
    return """
    <a href="/fb-login">Login with Facebook</a>
    <a href="/google/login">Login with Google</a>
    """


# @app.route('/login', methods=['GET', 'POST'])
@app.route('/login')
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify you', 401,
                             {'Okoa Farmer Authentication': 'Basic realm: "login required"'})

    user = UserModel.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify you', 401,
                             {'Okoa Farmer Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'Okoa farmer Authentication': 'Basic realm: "login required"'})


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
    facebook_callback()


if __name__ == "__main__":
    from src.models.Model import db

    db.init_app(app)

    app.run(host='0.0.0.0', port=4000,debug=True)
