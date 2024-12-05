# app/models/user.py
from app import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True) 
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True) 
    username = db.Column(db.String(100), unique=True, nullable=True)
    mobile_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=True)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  
    otp_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    total_purchases = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    user_role = db.Column(db.String(50), default='customer')

    def __repr__(self):
        return f"<User  {self.username}>"

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)
