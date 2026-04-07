# app/models/__init__.py

from app import db  # ✅ Import the shared db from app/__init__.py

from .user import User  # ✅ Make sure this line is present
from .image_record import ImageRecord
from .missing import get_missing_person_model


MissingPerson = get_missing_person_model(db)