# config.py

class Config:
    SECRET_KEY = 'your-secret-key'  # Change this to a secure key
    SQLALCHEMY_DATABASE_URI = "postgresql://bhavaniboyapati@localhost:5432/abductor_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-jwt-secret-key'  # Change this too
 