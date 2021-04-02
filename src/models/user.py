from datetime import datetime
from src.database import db
from flask_marshmallow import Marshmallow

class User(db.Model):
  __tablename__ = 'user'
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String, unique=True)
  password = db.Column(db.String)
  ctime = db.Column(db.DateTime, default=datetime.now)
  utime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  
  def get(email):
    return db.session.query(User)\
      .filter(User.email == email)\
        .one()
  
  def post(uuid, email, password):
    new_user = User(id=uuid, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

ma = Marshmallow()
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'email', 'ctime', 'utime')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
