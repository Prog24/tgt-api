from datetime import datetime
from ..database import db
from flask_marshmallow import Marshmallow
import uuid as _uuid

class Diary(db.Model):
  __tablename__ = 'diary'
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.String, primary_key=True)
  user_id = db.Column(db.String)
  main_text = db.Column(db.String)
  sub_text = db.Column(db.Text)
  lat = db.Column(db.String)
  lon = db.Column(db.String)
  ctime = db.Column(db.DateTime, default=datetime.now)
  utime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  
  # 特定のユーザの日記全件取得
  def getByUser(uid):
    return db.session.query(Diary)\
      .filter(Diary.user_id == uid)\
      .order_by(Diary.ctime.desc())\
      .all()
  
  # 日記の作成
  def create(uid, main_text, sub_text, lat, lon):
    uuid = str(_uuid.uuid4())
    new_diary = Diary(id=uuid, user_id=uid, main_text=main_text, sub_text=sub_text, lat=lat, lon=lon)
    db.session.add(new_diary)
    db.session.commit()
    return new_diary
  
  # 特定の日記の更新
  def patch(did, uid, main_text, sub_text):
    tmp_diary = db.session.query(Diary)\
      .filter(Diary.id == did, Diary.user_id == uid)\
        .one()
    tmp_diary.main_text = main_text
    tmp_diary.sub_text = sub_text
    db.session.add(tmp_diary)
    db.session.commit()
  
  # 特定の日記の削除
  def delete(did, uid):
    delete_diary = db.session.query(Diary)\
      .filter(Diary.id == did, Diary.user_id == uid)\
        .one()
    print(delete_diary.id, delete_diary.user_id)
    db.session.delete(delete_diary)
    db.session.commit()

ma = Marshmallow()
class DiarySchema(ma.Schema):
  class Meta:
    fields = ('id', 'main_text', 'sub_text', 'lat', 'lon', 'ctime', 'utime')

diary_schema = DiarySchema()
diaries_schema = DiarySchema(many=True)
