from flask_restful import Resource, reqparse, abort
from flask import jsonify, make_response, request
from flask_jwt_extended import (
  jwt_required, get_jwt_identity
)
from src.models.diary import Diary, diary_schema, diaries_schema

class DiaryAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    super(DiaryAPI, self).__init__()
  
  # 特定のユーザの日記全件取得
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    try:
      diaries = Diary.getByUser(user_id)
    except:
      return make_response(jsonify({'error': 'not match'}), 400)
    return make_response(diaries_schema.jsonify(diaries), 200)
  
  # 日記の作成
  @jwt_required()
  def post(self):
    json = request.get_json()
    user_id = get_jwt_identity()
    if not json:
      return make_response(jsonify({'error': 'not content'}), 400)
    try:
      tmp = Diary.create(user_id, json.get('main_text'), json.get('sub_text'), json.get('lat'), json.get('lon'))
    except:
      return make_response(jsonify({'error': 'not match'}), 400)
    # return make_response(jsonify({'message':'success!'}), 200)
    return make_response(diary_schema.jsonify(tmp), 200)
