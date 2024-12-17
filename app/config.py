# app/config.py 
from decouple import config # type: ignore # load values from .env

class Config:
    SECRET_KEY = "9fdde50cf248cc178bac18fa6cb3e6de1510bcd207c5a4e3a1ec3d832eb44af0" 
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI", default="mysql+pymysql://root:@localhost/joskamodernmabati") 
    # Database connection URI
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://joskrpni_autocrat:Autocrat#2250229202019@localhost/joskrpni_joskamodernmabati"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/static/images"
    PRODUCT_UPLOAD_FOLDER = "app/static/images/products"
    CATEGORY_UPLOAD_FOLDER = "app/static/images/category"

    COMPANY_NAME = "JOSKA MODERN MABATI"
    COMPANY_PHONE_1 = "+254757398722"
    COMPANY_PHONE_2 = "+2540705152121"
    COMPANY_EMAIL_1 = "joskamodernmabati@gmail.com"
    COMPANY_URL = "https://joskamodernmabati.com/"

    # EMAIL SETUP
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "joskamodernmabati@gmail.com"
    MAIL_PASSWORD = "czss aznv udwx pnpu"
    MAIL_DEFAULT_SENDER = ("JOSKA MODERN MABATI", "joskamodernmabati@gmail.com")

    # TWILIO API SETUP
    TWILIO_ACCOUNT_SID = "AC2d2855337c0f6df2ca5c07604dd73b84"
    TWILIO_AUTH_TOKEN = "c4ca6d4998c57a4768ae8b41fe03969d"
    TWILIO_WHATSAPP_NUMBER = "whatsapp:+17753169385"  # Twilio's default WhatsApp number

    # TWILIO_ACCOUNT_SID = "SK8edb13bf70f43c382f6f99cafdfdfe06"
    # TWILIO_AUTH_TOKEN = "bKYlXzQWKzwR9rdY9KJUD8nQjLHpeb5d"
    
    # # TWILIO API SETUP - LIVE CREDENTIALS (USE THIS FOR PRODUCTION)
    # TWILIO_ACCOUNT_SID = "AC2d2855337c0f6df2ca5c07604dd73b84"
    # TWILIO_AUTH_TOKEN = "c4ca6d4998c57a4768ae8b41fe03969d"
    # TWILIO_WHATSAPP_NUMBER = "whatsapp:+17753169385"  # Twilio's default WhatsApp number

    #  # TWILIO API SETUP - TEST CREDENTIALS (USE THIS FOR TESTING ONLY)
    # # TWILIO_ACCOUNT_SID = "ACaccac560a7f5d6247772f6efa39c0dff"
    # # TWILIO_AUTH_TOKEN = "a630ee52aa02df33ab413832a64dd7b8"
    # # TWILIO_WHATSAPP_NUMBER = "whatsapp:+17753169385"  # Twilio's default WhatsApp number