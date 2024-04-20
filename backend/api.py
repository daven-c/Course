from flask import request, jsonify
from config import app, db
from models import Student


@app.route("/get_student/<string:dir_id>", methods=["GET"])
def get_student(dir_id):
    student = Student.query.get(dir_id)
    if student is None:
        return jsonify({"message": f"{dir_id} not found"}, 404)
    return jsonify({"message": f"{dir_id} found", "student": student.to_json()}), 200


@app.route("/create_student/<string:dir_id>", methods=["POST"])
def create_student(dir_id):
    new_student = Student(dir_id=dir_id)
    try:
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Student created"}), 201


@app.route("/update_student", methods=["PUT"])
def update_student():
    data = request.get_json()  # Get JSON data
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400

    dir_id = data.get("dir_id")
    if not dir_id:
        return jsonify({"message": "dir_id is required"}), 400

    # Fetch student (with error handling)
    student = get_student(dir_id=dir_id)
    if not student:
        return jsonify({"message": f"{dir_id} not found"}), 404

    for attr in ["first_name", "last_name", "insta_handle"]:
        value = data.get(attr)
        if value is None:
            return jsonify({"message": f"{attr} is required"}), 400
        setattr(student, attr, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating student: {str(e)}"}), 500

    return jsonify({"message": "Student updated"}), 200


@app.route("/update_courses/<string:dir_id>", methods=["PUT"])
def update_courses(dir_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400

    new_courses = data.get("courses")
    if not new_courses or not isinstance(new_courses, list):
        return jsonify({"message": "Invalid course list provided"}), 400

    student = get_student(dir_id=dir_id)
    if not student:
        return jsonify({"message": f"{dir_id} not found"}), 404

    # Clear existing courses
    for i in range(1, 9):
        setattr(student, f"course{i}", None)

    # Add new courses (with length check)
    if len(new_courses) > 8:
        return jsonify({"message": "Maximum 8 courses allowed"}), 400
    for i, course in enumerate(new_courses, 1):
        setattr(student, f"course{i}", course)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating courses: {str(e)}"}), 500

    return jsonify({"message": "Courses updated"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
