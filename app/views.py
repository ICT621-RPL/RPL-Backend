from flask import request, jsonify
from app import app, db, ma
from app.models import Experience

class ExperienceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Experience
        sqla_session = db.session

experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)

@app.route('/experience', methods=['POST'])
def add_experience():
    studentId = request.json['studentId']
    jobTitle = request.json['jobTitle']
    fromDate = request.json['fromDate']
    toDate = request.json['toDate']
    experience = request.json['experience']

    new_experience = Experience(studentId, jobTitle, fromDate, toDate, experience)
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
        experience.from_date = request.json.get('fromDate', experience.from_date)
        experience.to_date = request.json.get('toDate', experience.to_date)
        experience.experience = request.json.get('experience', experience.experience)

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
