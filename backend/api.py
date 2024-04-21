from flask import request, jsonify
from config import app, db
from models import Student
import json
from utils.schedule_finder import get_course_list


@app.route("/get_student/<string:dir_id>", methods=["GET"])
def get_student(dir_id):
    student = Student.query.get(dir_id)
    if student is None:
        return jsonify({"message": f"{dir_id} not found"}), 404
    return jsonify({"message": f"{dir_id} found", "student": student.to_json()}), 200


@app.route("/get_connections/<string:dir_id>", methods=["GET"])
def get_connections(dir_id):
    connections = []
    student = Student.query.get(dir_id)
    student_courses = {value for key, value in student.__dict__.items(
    ) if key.startswith('course') and value != None}
    for connection in Student.query.all():  
        if student.dir_id != connection.dir_id:
            connection_courses = {value for key, value in connection.__dict__.items(
            ) if key.startswith('course') and value != None}
            shared_courses = student_courses.intersection(connection_courses)
            connections.append([connection.dir_id, list(shared_courses)])
    return jsonify({"connections": connections}), 200


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
        update_courses(dir_id, course_list)
        return response
    else:
        update_courses(dir_id, course_list)
        return jsonify({"message": "authentication success"}), 200


def create_student(dir_id):
    new_student = Student(dir_id=dir_id)
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created"}), 201


@app.route("/update_student", methods=["PUT"])
def update_student():
    dir_id = request.json.get("dir_id")
    full_name = request.json.get("full_name")
    insta_handle = request.json.get("insta_handle")

    student = Student.query.get(dir_id)
    student.full_name = full_name
    student.insta_handle = insta_handle

    db.session.commit()

    return jsonify({"message": "Student updated"}), 200


def update_courses(dir_id, courseList):
    student = Student.query.get(dir_id)

    if len(courseList) > 8:
        return jsonify({"message": "failed to update course list"}, 417)

    for i, course in enumerate(courseList):
        setattr(student, f"course{i + 1}", course)

    db.session.commit()

@app.route("/delete_student/<string:dir_id>", methods=["GET"])
def delete_student(dir_id):
    student = Student.query.get(dir_id)
    if student is None:
        return jsonify({"message": f"{dir_id} not found"}), 404

    try:
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting student: {str(e)}"}), 500

    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
