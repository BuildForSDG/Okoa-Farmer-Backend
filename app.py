import json
import logging
import os
import sys

import config
from src.models.Model import db

from src import google_auth
from src.resources.farmer_rating import FarmerRatingRegister, FarmerRatingFilter, FarmerRatingIDFilter
from src.resources.item import ItemRegister, ItemFilter
from src.resources.item_category import ItemCategoryRegister, ItemCategoryFilter

# sys.path.insert(0, './src')
import bcrypt
import flask
import requests_oauthlib
from flask import Flask, request
from flask import jsonify
from flask_jwt import JWTError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token
)
from flask_restful import Api
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from src.google_auth import google_auth_redirect
from src.google_auth import logout
from src.models.user import UserModel
from src.resources.permission import PermissionRegister, PermissionFilter
from src.resources.role import RoleRegister, RoleFilter
from src.resources.role_permission import RolePermissionRegister, RolePermissionFilter
from src.resources.user import UserRegister, UserFilter
from src.resources.user_role import UserRoleRegister, UserRoleFilter

app = Flask(__name__)
app.config.from_object('config')
# local
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY  # to encode cookies
db.init_app(app)
api = Api(app)

# log system errors
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

jwt = JWTManager(app)


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}, 401)


############################### Resource Routes for Okoa Farmer ################################
# user registration
api.add_resource(UserRegister, '/register')
api.add_resource(UserFilter, '/register/<string:id>')
# permissions
api.add_resource(PermissionRegister, '/permissions')
api.add_resource(PermissionFilter, '/permissions/<string:name>')
# roles
api.add_resource(RoleRegister, '/roles')
api.add_resource(RoleFilter, '/roles/<string:id>')
# user roles
api.add_resource(UserRoleRegister, '/user/roles')
api.add_resource(UserRoleFilter, '/user/roles/<string:userid>/<string:roleid>')
# role permissions
api.add_resource(RolePermissionRegister, '/role/permissions')
api.add_resource(RolePermissionFilter, '/role/permissions/<string:roleid>/<string:permissionid>')
# item
api.add_resource(ItemRegister, '/item')
api.add_resource(ItemFilter, '/item/<string:id>')
# item category
api.add_resource(ItemCategoryRegister, '/item/category')
api.add_resource(ItemCategoryFilter, '/item/category/<string:categoryname>')
# farmer rating
api.add_resource(FarmerRatingRegister, '/farmer/rating')
api.add_resource(FarmerRatingIDFilter, '/farmer/rating/<string:id>')
api.add_resource(FarmerRatingFilter, '/rating/<string:farmerid>/<string:itemid>/<string:ratedby>')


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
            # access_token = create_access_token(identity={"username": username})
            access_token = create_access_token(identity={"username": username, "password": password})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide a Username and Password in JSON format in the request body', 400


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


@app.route("/kujuana", methods=['GET'])
# @jwt_required
def testing_things():
    return "Testing tings!!!!!!"


#############################################START OF FACEBOOK OAUTH #################################################

# Your ngrok url, obtained after running "ngrok http 5000"
URL = "https://okoafarmer.herokuapp.com"
# URL = "https://8b335cb8a43d.ngrok.io"

FB_CLIENT_ID = os.environ.get("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.environ.get("FB_CLIENT_SECRET")

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FB_SCOPE = ["email"]

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# app = flask.Flask(__name__)

@app.route("/fb-login")
def facebook_login():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)
    return flask.redirect(authorization_url)
    # return jsonify(authorization_url)


@app.route("/fb-callback")
def facebook_callback():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=flask.request.url,
    )

    # Fetch a protected resource, i.e. user profile, via Graph API
    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data["email"]
    name = facebook_user_data["name"]
    picture_url = facebook_user_data.get("picture", {}).get("data", {}).get("url")

    return jsonify({'name': name, 'email': email, 'img': picture_url, 'message': 'You have logged in successfully'})
#
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=9000, debug=True)
