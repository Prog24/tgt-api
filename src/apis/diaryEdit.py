from flask_restful import Resource, reqparse, abort
from flask import jsonify, make_response, request
from flask_jwt_extended import (
  jwt_required, get_jwt_identity
)
from src.models.diary import Diary, diary_schema, diaries_schema

class DiaryEditAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    super(DiaryEditAPI, self).__init__()
  
  # 特定の日記の更新
  @jwt_required()
  def patch(self, diary_id):
    json = request.get_json()
    user_id = get_jwt_identity()
    if not json:
      return make_response(jsonify({'error': 'not content'}), 400)
    try:
      Diary.patch(diary_id, user_id, json.get('main_text'), json.get('sub_text'))
    except Exception:
      return make_response(jsonify({'error': 'not match'}), 400)
    return make_response(jsonify({'message':'success'}), 200)
  
  # 特定の日記の削除
  @jwt_required()
  def delete(self, diary_id):
    user_id = get_jwt_identity()
    try:
      Diary.delete(diary_id, user_id)
    except Exception:
      return make_response(jsonify({'error': 'not match'}), 400)
    return make_response(jsonify({'message':'success delete'}), 200)
