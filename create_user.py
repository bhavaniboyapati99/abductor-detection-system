from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    email_or_mobile = "testuser@example.com"
    password = "1234"

    user = User.query.filter_by(email_or_mobile=email_or_mobile).first()
    if not user:
        new_user = User(email_or_mobile=email_or_mobile, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        print("User created!")
    else:
        print("User already exists.")
