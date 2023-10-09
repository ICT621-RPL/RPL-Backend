import os
from flask import request, jsonify
from app import app, db, ma
from werkzeug.utils import secure_filename
from app.models import Experience, ExperienceDocument, Recommendation, RplApplication
from app.utils import allowed_file, experience_to_dict, recommendation_to_dict
from app.ml import cosine_similarity_check, compute_model


class ExperienceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Experience
        sqla_session = db.session


experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)


class ExperienceDocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExperienceDocument
        sqla_session = db.session


experience_document_schema = ExperienceDocumentSchema()
experiences_document_schema = ExperienceDocumentSchema(many=True)


class RecommendationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recommendation
        sqla_session = db.session


recommendation_schema = RecommendationSchema()
recommendations_schema = RecommendationSchema(many=True)


class RplApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RplApplication
        sqla_session = db.session


rplApplication_schema = RplApplicationSchema()


@app.route("/experience", methods=["POST"])
def add_experience():
    studentId = 0
    jobTitle = request.json["jobTitle"]
    fromMonth = request.json["from_month"]
    fromYear = request.json["from_year"]
    toMonth = request.json["to_month"]
    toYear = request.json["to_year"]
    company = request.json["company"]
    country = request.json["country"]
    description = request.json["description"]
    new_experience = Experience(
        studentId,
        jobTitle,
        fromMonth,
        fromYear,
        toMonth,
        toYear,
        company,
        country,
        description,
    )
    db.session.add(new_experience)
    db.session.commit()

    # recommendation = call the model function
    generated_recommendations = compute_model(description)

    new_recommendations = []

    # save recommendation into the database
    for recommendation in generated_recommendations:
        unitCode = recommendation

        new_recommendation = Recommendation(new_experience.experience_id, unitCode, 0)
        db.session.add(new_recommendation)

        # to_dict method to convert Recommendation object to a dictionary
        new_recommendations.append(new_recommendation)

    db.session.commit()

    # to_dict method to convert Experience & Recommendation object to a dictionary
    recommendation_dict = []
    experience_dict = (
        new_experience.to_dict()
        if hasattr(new_experience, "to_dict")
        else experience_to_dict(new_experience)
    )
    for recommendation in new_recommendations:
        recommendation_dict.append(
            recommendation.to_dict()
            if hasattr(recommendation, "to_dict")
            else recommendation_to_dict(recommendation)
        )

    new_json = {"experience": experience_dict, "recommendations": recommendation_dict}

    return jsonify(new_json)


@app.route("/experiences", methods=["POST"])
def add_experiences():
    experiences_data = request.json
    new_experiences = []

    for exp_data in experiences_data:
        experienceId = exp_data.get("experience_id")
        recommendations = exp_data["courses"]

        experience = Experience.query.get(experienceId)
        experience.student_id = exp_data.get("studentId", experience.student_id)
        experience.job_title = exp_data.get("jobTitle", experience.job_title)
        experience.from_month = exp_data.get("from_month", experience.from_month)
        experience.from_year = exp_data.get("from_year", experience.from_year)
        experience.to_month = exp_data.get("to_month", experience.to_month)
        experience.to_year = exp_data.get("to_year", experience.to_year)
        experience.company = exp_data.get("company", experience.company)
        experience.country = exp_data.get("country", experience.country)
        experience.description = exp_data.get("description", experience.description)

        for recommendation in recommendations:
            existing_recommendation = Recommendation.query.get(recommendation)
            existing_recommendation.experience_id = experienceId
            existing_recommendation.is_applied = 1
            recommendations.append(existing_recommendation)
        

    db.session.commit()
    return experiences_schema.jsonify(new_experiences)


@app.route("/upload", methods=["POST"])
def upload_files():
    experience_id = request.form.get(
        "experience_id"
    )  # Get the experience ID from the form data
    if not experience_id:
        return jsonify({"error": "Experience ID not provided"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist("file")
    saved_files = []

    for file in files:
        if file.filename == "":
            continue

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filePath)
            saved_files.append(filename)

            new_experience_document = ExperienceDocument(
                experience_id, filename, filePath
            )
            db.session.add(new_experience_document)
        else:
            return jsonify({"error": f"File type not allowed for {file.filename}"}), 400

    if not saved_files:
        return jsonify({"error": "No valid files to save"}), 400

    db.session.commit()
    return jsonify(
        {
            "message": "Files uploaded successfully!",
            "filenames": saved_files,
            "experience_id": experience_id,
        }
    )


@app.route("/application", methods=["POST"])
def add_application():
    studentId = request.json["studentId"]
    experienceId = request.json["experienceId"]

    if not experienceId:
        return jsonify({"error": "Experience ID not provided"}), 400
    elif not studentId:
        return jsonify({"error": "Student ID not provided"}), 400
    else:
        new_application = RplApplication(None, studentId, experienceId)
        db.session.add(new_application)
        db.session.commit()


@app.route("/experiences", methods=["GET"])
def get_experiences():
    all_experiences = Experience.query.all()
    return experiences_schema.jsonify(all_experiences)


@app.route("/experience/<id>", methods=["GET"])
def get_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        return experience_schema.jsonify(experience)


@app.route("/experience/<id>", methods=["PUT"])
def update_experience(id):
    experience = Experience.query.get(id)

    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        experience.student_id = (
            0  # request.json.get('studentId', experience.student_id)
        )
        experience.job_title = request.json.get("jobTitle", experience.job_title)
        experience.from_month = request.json.get("from_month", experience.from_month)
        experience.from_year = request.json.get("from_year", experience.from_year)
        experience.to_month = request.json.get("to_month", experience.to_month)
        experience.to_year = request.json.get("to_year", experience.to_year)
        experience.company = request.json.get("company", experience.company)
        experience.country = request.json.get("country", experience.country)
        experience.description = request.json.get("experience", experience.description)

        db.session.commit()
        return experience_schema.jsonify(experience)


@app.route("/experience/<id>", methods=["DELETE"])
def delete_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        db.session.delete(experience)
        db.session.commit()
        return experience_schema.jsonify(experience)
