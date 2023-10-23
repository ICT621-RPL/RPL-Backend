import os
from flask import request, jsonify, abort
from app import app, db, ma
from werkzeug.utils import secure_filename
from app.models import (
    Experience,
    ExperienceDocument,
    Recommendation,
    RplApplication,
    Status,
)
from app.utils import allowed_file, send_email, recommendation_to_dict
from app.ml import cosine_similarity_with_knn


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


class StatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Status
        sqla_session = db.session


statuses_schema = StatusSchema(many=True)


@app.route("/experience", methods=["POST"])
def add_experience():
    fromYear = request.json["from_year"]
    toYear = request.json["to_year"]
    description = request.json["description"]

    # Validate that fromYear is less than toYear
    if fromYear >= toYear:
        abort(400, description="From year must be less than To year")

    # recommendation = call the model function
    generated_recommendations = cosine_similarity_with_knn(description)

    # Convert generated recommendations to json object
    recommendations = recommendation_to_dict(generated_recommendations)

    new_json = {"experience": request.json, "recommendations": recommendations}

    return jsonify(new_json)


@app.route("/experiences", methods=["POST"])
def add_experiences():
    student_id = request.json["studentId"]
    experiences_data = request.json["experiences"]

    new_application = RplApplication(None, student_id)
    db.session.add(new_application)
    db.session.commit()

    for exp_data in experiences_data:
        jobTitle = exp_data.get("jobTitle")
        fromMonth = exp_data.get("from_month")
        fromYear = exp_data.get("from_year")
        toMonth = exp_data.get("to_month")
        toYear = exp_data.get("to_year")
        company = exp_data.get("company")
        country = exp_data.get("country")
        description = exp_data.get("description")

        new_experience = Experience(
            student_id,
            jobTitle,
            fromMonth,
            fromYear,
            toMonth,
            toYear,
            company,
            country,
            description,
            new_application.application_id,
        )
        db.session.add(new_experience)
        db.session.commit()

        recommendations = exp_data["courses"]
        for recommendation in recommendations:
            new_recommendation = Recommendation(
                new_experience.experience_id,
                recommendation.get('recommendation_unit_code'),
                recommendation.get('recommendation_unit_name'),
                recommendation.get('recommendation_similarity'),
                1,
                1,
            )
            db.session.add(new_recommendation)
            db.session.commit()

    return rplApplication_schema.jsonify(new_application)


@app.route("/upload", methods=["POST"])
def upload_files():
    application_id = request.form.get(
        "application_id"
    )  # Get the application ID from the form data

    if not application_id:
        return jsonify({"error": "Application ID not provided"}), 400

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
                application_id, filename, filePath
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
            "application_id": application_id,
        }
    )


@app.route("/application", methods=["POST"])
def submit_application():
    application_id = request.json["application_id"]
    all_experience_documents = ExperienceDocument.query.filter_by(
        application_id=application_id
    ).all()
    application = RplApplication.query.get(application_id)
    all_experiences = Experience.query.filter_by(
        student_id=application.student_id
    ).all()

    all_recommendations = []
    for experience in all_experiences:
        all_recommendations.append(
            Recommendation.query.filter_by(experience_id=experience.experience_id)
        )

    send_email(
        application_id, all_experiences, all_experience_documents, all_recommendations
    )
    return jsonify({"Message": "Application successfully submitted"}), 200


@app.route("/application/<id>", methods=["GET"])
def get_application(id):
    application = RplApplication.query.get(id)

    if not application:
        return jsonify({"error": "Application not found"}), 404
    else:
        all_experiences = Experience.query.filter_by(
            application_id=application.application_id
        ).all()
        application_data = rplApplication_schema.dump(application)
        experiences_data = []

        for experience in all_experiences:
            experience_data = experience_schema.dump(experience)

            # Query recommendations with is_applied = 1 for this experience
            recommendations = Recommendation.query.filter_by(
                experience_id=experience.experience_id, is_applied=1
            ).all()
            recommendation_data = []

            for rec in recommendations:
                status = Status.query.get(rec.status_id)  # Fetch status information
                recommendation_dict = recommendation_schema.dump(rec)
                recommendation_dict["status_id"] = status.status_id
                recommendation_dict["status_name"] = status.status_name
                recommendation_data.append(recommendation_dict)

            experience_data["recommendations"] = recommendation_data
            experiences_data.append(experience_data)

        return jsonify(
            {"application": application_data, "experiences": experiences_data}
        )


@app.route("/experience/<id>", methods=["DELETE"])
def delete_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        db.session.delete(experience)
        db.session.commit()
        return experience_schema.jsonify(experience)


@app.route("/recommendation", methods=["POST"])
def add_recommendation():
    unit_code = request.json["unit_code"]
    unit_name = request.json["unit_name"]
    experience_id = request.json["experience_id"]

    new_recommendation = Recommendation(experience_id, unit_code, unit_name, None, 1, 2)
    db.session.add(new_recommendation)
    db.session.commit()

    return recommendation_schema.jsonify(new_recommendation)


@app.route("/transaction", methods=["POST"])
def change_status():
    recommendation_id = request.json["recommendation_id"]
    status_id = request.json["status_id"]

    recommendation = Recommendation.query.get(recommendation_id)

    if not recommendation:
        return jsonify({"error": "Recommendation not found"}), 404
    else:
        recommendation.status_id = status_id
        db.session.commit()

        return recommendation_schema.jsonify(recommendation)


@app.route("/statuses", methods=["GET"])
def get_statues():
    all_statuses = Status.query.all()
    return statuses_schema.jsonify(all_statuses)


@app.route("/download/<int:application_id>", methods=["GET"])
def download_files(application_id):
    documents = ExperienceDocument.query.filter_by(application_id=application_id).all()

    if not documents:
        return (
            jsonify({"error": "No documents found for the given application ID"}),
            404,
        )

    # Create a list to store file information
    file_data = []

    for document in documents:
        file_id = document.document_id
        file_name = document.file_name
        file_path = document.file_path

        # Read the file content
        with open(file_path, "rb") as file:
            file_content = file.read()

        file_data.append(
            {
                "file_id": file_id,
                "file_name": file_name,
                "file_content": file_content.decode(
                    "latin-1"
                ),  # Convert binary content to a string
                "file_path": file_path,
            }
        )

    return jsonify(file_data)
