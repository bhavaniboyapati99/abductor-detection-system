# app/models/missing.py
from app import db  # ✅ Correct import
def get_missing_person_model(db):
    class MissingPerson(db.Model):
        __tablename__ = 'missing_persons'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        date_of_birth = db.Column(db.Date)
        gender = db.Column(db.String(10))
        last_seen = db.Column(db.DateTime)
        last_seen_place = db.Column(db.String(255))  # ✅ Add this line
        description = db.Column(db.Text)
        photo_path = db.Column(db.String(255))
        reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
        status = db.Column(db.String(20), default='missing')

        # ✅ Add this line to track creation time
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    return MissingPerson
