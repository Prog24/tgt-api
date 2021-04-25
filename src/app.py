from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import (
  JWTManager,
)
from .database import db
from .config import Config

from src.apis.diary import DiaryAPI
from src.apis.diaryEdit import DiaryEditAPI
from src.apis.happySpots import HappySpotAPI
from src.apis.auth import (LoginAPI, RegisterAPI, RefreshAPI)

def create_app():
  app = Flask(__name__)
  app.config['JSON_AS_ASCII'] = False
  app.config['JWT_SECRET_KEY'] = 'super-secret'
  app.config['JWT_TOKEN_LOCATION'] = ['headers']
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 2592000
  app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000 * 3
  jwt = JWTManager(app)
  app.config.from_object(Config)
  db.init_app(app)

  cors = CORS(app, resources={r"*": {"origins":"*"}})
  api = Api(app)

  api.add_resource(DiaryAPI, '/diary')
  api.add_resource(DiaryEditAPI, '/diary/<diary_id>')
  api.add_resource(HappySpotAPI, '/spots')
  api.add_resource(LoginAPI, '/auth/login')
  api.add_resource(RegisterAPI, '/auth/register')
  api.add_resource(RefreshAPI, '/auth/refresh')

  return app

app = create_app()
