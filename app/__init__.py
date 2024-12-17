# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_mail import Mail
from twilio.rest import Client  # Twilio import
from flask import current_app

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load configuration from Config class
    
    # Initialize Twilio Client
    twilio_client = Client(
        app.config['TWILIO_ACCOUNT_SID'], 
        app.config['TWILIO_AUTH_TOKEN']
    )
    app.twilio_client = twilio_client  # This makes it accessible in the entire app

    # session for cart
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"  # Store session data on server
    Session(app)

    # Context Processor for global template variables
    @app.context_processor
    def inject_company_name():
        return {
            'company_name': app.config['COMPANY_NAME'],
            'company_email_1': app.config['COMPANY_EMAIL_1'],
            'company_email_2': app.config['COMPANY_EMAIL_2'],
            'company_phone_1': app.config['COMPANY_PHONE_1'],
            'company_phone_2': app.config['COMPANY_PHONE_2'],
            'company_url': app.config['COMPANY_URL']
        }

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = "auth.login"  # Adjust this based on your blueprint

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))  # Load user by ID

    # Register blueprints
    from app.views.admin import admin as admin_blueprint
    from app.views import main as main_blueprint
    from app.views.auth import auth as auth_blueprint
    from app.views.cart import cart as cart_blueprint
    from app.views.products import ecommerce as product_blueprint

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(product_blueprint)

    return app


# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

# flask db current
# flask db downgrade

# flask db history