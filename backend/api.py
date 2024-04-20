from flask import request, jsonify
from config import app, db
from models import Student
from utils.schedule_finder import get_course_list


@app.route("/get_student/<string:dir_id>", methods=["GET"])
def get_student(dir_id):
    student = Student.query.get(dir_id)
    if student is None:
        return jsonify({"message": f"{dir_id} not found"}), 404
    return jsonify({"message": f"{dir_id} found", "student": student.to_json()}), 200


@app.route("/auth_student", methods=["POST"])
def auth_student():
    dir_id = request.json.get("dirID")
    password = request.json.get("password")

    course_list = get_course_list(dir_id, password)

    if course_list is None:  # Auth failed
        return jsonify({"message": "auth failed"}), 404

    student = Student.query.get(dir_id)
    if student is None:  # Student doesn't exist yet
        response = create_student(dir_id)
        return response
    else:
        return jsonify({"message": "authentication success"}), 200


def create_student(dir_id):
    new_student = Student(dir_id=dir_id)
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created"}), 201


@app.route("/update_student", methods=["PUT"])
def update_student():
    dir_id = request.json.get("dir_id")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last name")
    insta_handle = request.json.get("insta_handle")

    student = Student.query.get(dir_id)
    student.first_name = first_name
    student.last_name = last_name
    student.insta_handle = insta_handle

    db.session.commit()

    return jsonify({"message": "Student updated"})


@app.route("/update_courses/<string:dir_id>", methods=["PUT"])
def update_courses(dir_id):
    # Get courses related to dir_id
    new_courses = ...  # Yet to be implemented

    student = Student.query.get(dir_id)

    if len(new_courses) > 8:
        return jsonify({"message": "failed to update course list"}, 417)

    for i, course in enumerate(course_list):
        setattr(student, f"course{i+len(existing_courses)+1}", course)

    db.session.commit()

    return jsonify({"message": "User updated"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
