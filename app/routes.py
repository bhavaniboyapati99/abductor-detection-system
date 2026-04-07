import os
import uuid
import numpy as np
from PIL import Image

from flask import Blueprint, request, jsonify, current_app, render_template, url_for
from werkzeug.utils import secure_filename

from tensorflow.keras.models import load_model

from app.models import db, ImageRecord, MissingPerson
from flask import url_for



# ---------------------------------
# Blueprint
# ---------------------------------
main_bp = Blueprint('main', __name__)

model = None
CLASS_LABELS = None


# ---------------------------------
# Web Pages
# ---------------------------------
@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/police-login")
def police_login_page():
    return render_template("police-login.html")


@main_bp.route("/police-login", methods=["POST"])
def police_login():

    data = request.get_json()

    email_or_mobile = data.get("emailOrMobile")
    password = data.get("password")

    # demo admin login
    if email_or_mobile == "police" and password == "1234":
        return jsonify({
            "access_token": "demo-token",
            "role": "admin"
        })

    return jsonify({"error": "Invalid admin credentials"}), 401

@main_bp.route("/api/approve/<int:case_id>", methods=["POST"])
def approve_case(case_id):
    person = MissingPerson.query.get(case_id)

    if not person:
        return jsonify({"error": "Case not found"}), 404

    return jsonify({"message": "Approved successfully"})



@main_bp.route("/api/delete/<int:case_id>", methods=["DELETE"])
def delete_case(case_id):
    person = MissingPerson.query.get(case_id)

    if not person:
        return jsonify({"error": "Case not found"}), 404

    db.session.delete(person)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})


@main_bp.route("/upload-image")
def upload_image_page():
    return render_template("upload-image.html")


@main_bp.route("/register-case")
def register_case():
    return render_template("register-case.html")


@main_bp.route("/common-login")
def login_page():
    return render_template("common-login.html")


@main_bp.route("/police-dashboard")
def police_dashboard():
    return render_template("police-dashboard.html")


# ---------------------------------
# Load CNN Model
# ---------------------------------
def get_model():
    global model

    if model is None:
        model_path = os.path.join(
            current_app.root_path,
            "models",
            "your_cnn_model.keras"
        )

        model = load_model(model_path)

    return model


# ---------------------------------
# Load class labels
# ---------------------------------
def get_class_labels():
    global CLASS_LABELS

    if CLASS_LABELS is None:

        labels_path = os.path.join(
            current_app.root_path,
            "models",
            "class_labels.txt"
        )

        with open(labels_path, "r") as f:
            CLASS_LABELS = [line.strip() for line in f.readlines()]

    return CLASS_LABELS


# ---------------------------------
# Image Preprocessing
# ---------------------------------
def preprocess_image(image_path, target_size=(224, 224)):

    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# ---------------------------------
# Predict image
# ---------------------------------
def predict_image(model, image_path):

    img_array = preprocess_image(image_path)

    preds = model.predict(img_array)

    return preds


# ---------------------------------
# Upload Image (General Prediction)
# ---------------------------------
@main_bp.route('/upload', methods=['POST'])
def upload_image():

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    print(f"🖼️ Image saved: {file_path}")

    # Load model
    model = get_model()
    CLASS_LABELS = get_class_labels()

    preds = predict_image(model, file_path)

    probs = preds[0]

    top_index = np.argmax(probs)
    confidence = float(probs[top_index])

    sorted_probs = np.sort(probs)

    margin = sorted_probs[-1] - sorted_probs[-2]

    predicted_label = CLASS_LABELS[top_index]

    # Unknown detection
    if confidence < 0.97 or margin < 0.25 or confidence > 0.9995:
        predicted_label = "Unknown Person"

    record = ImageRecord(
        filename=unique_filename,
        predicted_name=predicted_label,
        confidence=confidence,
        location="Unknown",
        uploaded_by="system"
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "message": "Image uploaded successfully",
        "filename": unique_filename,
        "prediction": predicted_label,
        "confidence": confidence
    })


# ---------------------------------
# Register Missing Person
# ---------------------------------
@main_bp.route('/register-missing', methods=['POST'])
def register_missing():

    name = request.form.get("name")
    location = request.form.get("location")
    description = request.form.get("description")
    last_seen = request.form.get("last_seen")

    if 'image' not in request.files:
        return jsonify({"error": "Image required"}), 400

    file = request.files['image']

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads"
    )
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    missing_person = MissingPerson(
        name=name,
        last_seen = last_seen,
        last_seen_place=location,
        description=description,
        photo_path=unique_filename
    )

    db.session.add(missing_person)
    db.session.commit()

    return jsonify({
        "message": "Missing person registered successfully",
        "photo_path": unique_filename
    })

# ---------------------------------
# Get Missing Persons for Dashboard
# ---------------------------------
@main_bp.route('/api/missing-persons', methods=['GET'])
def get_missing_persons():

    persons = MissingPerson.query.all()

    results = []

    for person in persons:

        photo_url = None

        if person.photo_path:
            photo_url = url_for(
                'static',
                filename='uploads/' + person.photo_path
            )

        results.append({
            "id": person.id,
            "name": person.name,
            "last_seen_place": person.last_seen_place,
            "description": person.description,
            "photo_url": photo_url,
            "last_seen": person.last_seen if person.last_seen else "Unknown",
            "timestamp": "Recently Added"
        })

    return jsonify(results)

#suspicious case to upload in police dashboard#

@main_bp.route('/api/suspicious-reports', methods=['GET'])
def get_suspicious_reports():

    reports = ImageRecord.query.order_by(ImageRecord.timestamp.desc()).all()

    results = []

    for report in reports:
        photo_url = None

        if report.filename:
            photo_url = url_for(
                'static',
                filename='uploads/' + report.filename
            )

        results.append({
            "id": report.id,
            "predicted_name": report.predicted_name if report.predicted_name else "Unknown",
            "confidence": float(report.confidence) if report.confidence is not None else 0.0,
            "location": report.location if report.location else "Unknown",
            "description": report.description if report.description else "No description",
            "photo_url": photo_url,
            "timestamp": report.timestamp.strftime("%Y-%m-%d %H:%M:%S") if report.timestamp else "Unknown"
        })

    return jsonify(results)
# ---------------------------------
# Upload Suspicious Image
# ---------------------------------
@main_bp.route('/upload-suspicious', methods=['POST'])
def upload_suspicious():

    location = request.form.get("location")
    description = request.form.get("description")
    last_seen = request.form.get("last_seen")

    if 'image' not in request.files:
        return jsonify({"error": "Image required"}), 400

    file = request.files['image']

    filename = secure_filename(file.filename)
    unique_filename = f"suspicious_{uuid.uuid4().hex}_{filename}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    print(f"🚨 Suspicious image saved: {file_path}")

    # Load CNN model
    model = get_model()

    suspicious_features = model.predict(
        preprocess_image(file_path)
    )[0]

    best_match = None
    best_score = -1

    # Check how many persons exist in DB
    missing_persons = MissingPerson.query.all()
    print("Total missing persons in DB:", len(missing_persons))

    for person in missing_persons:
        print("Checking person:", person.name)

        person_image_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            person.photo_path
        )

        print("Image path:", person_image_path)

        if not os.path.exists(person_image_path):
            print("Image not found for:", person.name)
            continue

        person_features = model.predict(
            preprocess_image(person_image_path)
        )[0]

        similarity = np.dot(
            suspicious_features,
            person_features
        ) / (
            np.linalg.norm(suspicious_features)
            * np.linalg.norm(person_features)
        )

        print("Similarity with", person.name, ":", similarity)

        if similarity > best_score:
            best_score = similarity
            best_match = person

    matched_name = "Unknown"
    matched_photo = None

    if best_match and best_score > 0.7:
        matched_name = best_match.name
        matched_photo = best_match.photo_path
        print("Match found:", best_match.name)
    else:
        print("No match found. Best score:", best_score)

    # Save suspicious upload in ImageRecord table
    record = ImageRecord(
        filename=unique_filename,
        predicted_name=matched_name,
        confidence=float(best_score),
        location=location or "Unknown",
        description=description,
        uploaded_by="system"
    )

    db.session.add(record)
    db.session.commit()

    # Return result
    if matched_name != "Unknown":
        return jsonify({
            "match_found": True,
            "person_name": matched_name,
            "confidence": float(best_score),
            "photo_path": matched_photo,
            "location": location,
            "description": description,
            "last_seen": last_seen
        })

    return jsonify({
        "match_found": False,
        "confidence": float(best_score),
        "location": location,
        "description": description,
        "last_seen": last_seen
    })