# app/config.py 
from decouple import config # type: ignore # load values from .env

class Config:
    SECRET_KEY = config("SECRET_KEY", default="fallback_secret_key")
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI", default="mysql+pymysql://root:@localhost/joskamodernmabati") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False