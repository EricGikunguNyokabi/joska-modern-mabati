# app/config.py 
from decouple import config # type: ignore # load values from .env

class Config:
    SECRET_KEY = config("SECRET_KEY", default="fallback_secret_key")
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI", default="mysql+pymysql://root:@localhost/joskamodernmabati") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/static/images"
    PRODUCT_UPLOAD_FOLDER = "app/static/images/products"
    CATEGORY_UPLOAD_FOLDER = "app/static/images/category"

    COMPANY_NAME = "Joska Modern Mabati"
    COMPANY_PHONE_1 = "+254757398722"
    COMPANY_PHONE_2 = ""
    COMPANY_EMAIL_1 = "joskamodernmabati@gmail.com"
    COMPANY_URL = "https://joskamodernmabati.com/"