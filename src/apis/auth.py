from flask_restful import Resource, reqparse, abort
from flask import jsonify, make_response, request
from flask_jwt_extended import (
  create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
)
from flask_bcrypt import Bcrypt
import uuid as _uuid
from src.models.user import User, user_schema

class LoginAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('email', required=True)
    self.reqparse.add_argument('password', required=True)
    super(LoginAPI, self).__init__()

  def get(self):
    args = self.reqparse.parse_args()
    bcrypt = Bcrypt()
    try:
      user = User.get(args.email)
    except:
      return make_response(jsonify({'error': 'not match'}), 400)
    if not bcrypt.check_password_hash(user.password, args.password):
      return make_response(jsonify({'error': 'not match password'}), 400)
    access_token  = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    out_json = {
      'access_token': access_token,
      'refresh_token': refresh_token
    }
    return make_response(jsonify(out_json), 200)

class RegisterAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    super(RegisterAPI, self).__init__()
  
  def post(self):
    uuid = str(_uuid.uuid4())
    json = request.get_json()
    bcrypt = Bcrypt()
    if not json:
      return make_response(jsonify({'error': 'not match'}), 400)
    try:
      password = bcrypt.generate_password_hash(json.get('password')).decode('utf-8')
      User.post(uuid, json.get('email'), password)
    except:
      return make_response(jsonify({'error': 'not create'}), 400)
    access_token  = create_access_token(identity=uuid)
    refresh_token = create_refresh_token(identity=uuid)
    out_json = {
      'access_token': access_token,
      'refresh_token': refresh_token
    }
    return make_response(jsonify(out_json), 200)

class RefreshAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    super(RefreshAPI, self).__init__()
  
  @jwt_required(refresh=True)
  def get(self):
    user_id = get_jwt_identity()
    out_json = {
      'access_token': create_access_token(identity=user_id)
    }
    return make_response(jsonify(out_json), 200)
