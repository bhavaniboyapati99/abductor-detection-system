# reset_db.py

from app import create_app, db
from app.models.image_record import ImageRecord
from app.models.user import User  # include any models you need

def reset_database():
    app = create_app()  # create the Flask app instance
    with app.app_context():  # push the app context
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Done!")

if __name__ == "__main__":
    reset_database()
