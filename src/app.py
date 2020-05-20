from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt import JWT, JWTError
from src import google_auth
import json
from security import authenticate, identity
from src.resources.user import UserRegister
from src.google_auth import logout
from src.facebook_oauth import facebook_login, facebook_callback
from src.google_auth import google_auth_redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Masaki2017$$@localhost/okoafarmer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '#^#%^%&#BgdvttkkgyDDT&*%$' #to encode cookies
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


@app.route('/end')
def end_():
    return 'it is finally done'


if __name__ == "__main__":
    from src.models.Model import db

    db.init_app(app)

    app.run(host='0.0.0.0', port=4000)
