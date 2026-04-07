from . import db  # Correct: importing the db instance from __init__.py
from datetime import datetime

class ImageRecord(db.Model):
    __tablename__ = 'image_records'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    predicted_name = db.Column(db.String(120), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    last_seen_place = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    uploaded_by = db.Column(db.String(120), nullable=False)
    
    last_seen = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

     # ✅ Add this block
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reporter = db.relationship('User', backref='reported_cases')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.predicted_name,
            'photo_path': self.filename,
            'last_seen': self.last_seen.strftime("%Y-%m-%d %H:%M") if self.last_seen else None,
            'last_seen_place': self.last_seen_place,
            'description': self.description,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M") if self.timestamp else None,
        }
