from flask import request, jsonify
from app import app, db, ma
from app.models import Experience

class ExperienceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Experience
        sqla_session = db.session

experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)

@app.route('/experiences', methods=['POST'])
def add_experiences():
    experiences_data = request.json
    new_experiences = []

    for exp_data in experiences_data:
        studentId = exp_data.get('studentId', None)
        jobTitle = exp_data['jobTitle']
        fromMonth = exp_data['from_month']
        fromYear = exp_data['from_year']
        toMonth = exp_data['to_month']
        toYear = exp_data['to_year']
        company = exp_data['company']
        country = exp_data['country']
        description = exp_data['description']

        new_experience = Experience(studentId, jobTitle, fromMonth, fromYear, toMonth, toYear, company, country, description)
        db.session.add(new_experience)
        new_experiences.append(new_experience)

    db.session.commit()
    return experiences_schema.jsonify(new_experiences)

@app.route('/experience', methods=['POST'])
def add_experience():
    studentId = request.json['studentId']
    jobTitle = request.json['jobTitle']
    fromMonth = request.json['from_month']
    fromYear = request.json['from_year']
    toMonth = request.json['to_month']
    toYear = request.json['to_year']
    company = request.json['company']
    country = request.json['country']
    description = request.json['description']
    new_experience = Experience(studentId, jobTitle, fromMonth, fromYear, toMonth, toYear, company, country, description)
    db.session.add(new_experience)
    db.session.commit()
    return experience_schema.jsonify(new_experience)

@app.route('/experience', methods=['GET'])
def get_experiences():
    all_experiences = Experience.query.all()
    return experiences_schema.jsonify(all_experiences)

@app.route('/experience/<id>', methods=['GET'])
def get_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        return experience_schema.jsonify(experience)

@app.route('/experience/<id>', methods=['PUT'])
def update_experience(id):
    experience = Experience.query.get(id)

    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        experience.student_id = request.json.get('studentId', experience.student_id)
        experience.job_title = request.json.get('jobTitle', experience.job_title)
        experience.from_month = request.json.get('from_month', experience.from_month)
        experience.from_year = request.json.get('from_year', experience.from_year)
        experience.to_month = request.json.get('to_month', experience.to_month)
        experience.to_year = request.json.get('to_year', experience.to_year)
        experience.company = request.json.get('company', experience.company)
        experience.country = request.json.get('country', experience.country)
        experience.description = request.json.get('experience', experience.description)

        db.session.commit()
        return experience_schema.jsonify(experience)

@app.route('/experience/<id>', methods=['DELETE'])
def delete_experience(id):
    experience = Experience.query.get(id)
    if not experience:
        return jsonify({"error": "Experience not found"}), 404
    else:
        db.session.delete(experience)
        db.session.commit()
        return experience_schema.jsonify(experience)
