import os
class SystemConfig:
  DEBUG = True

  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db-name}?charset=utf8'.format(**{
    'user': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'db-name': os.environ['DB_NAME']
  })

Config = SystemConfig
