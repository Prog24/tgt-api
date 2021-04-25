from flask_restful import Resource, reqparse, abort
from flask import jsonify, make_response, request
from flask_jwt_extended import (
  jwt_required, get_jwt_identity
)
from src.models.user import User, user_schema

from src.utils.spot_rec import SpotRec
import os
import googlemaps

class HappySpotAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('lat', required=True)
    self.reqparse.add_argument('lon', required=True)
    super(HappySpotAPI, self).__init__()
  
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    user_info = User.getByID(user_id)
    user_name = user_info.email
    args = self.reqparse.parse_args()
    client = googlemaps.Client(os.environ['MAPS_API_KEY'])
    nearby = client.places_nearby(location=(args.lat, args.lon),radius=200,language='ja')
    geo_location = {}
    for data in nearby['results']:
      geo_location[data['place_id']] = client.place(data['place_id'], language='ja')
    out_data = SpotRec.pred_spot_score(user_name, geo_location)
    return make_response(jsonify({'message': out_data}), 200)

