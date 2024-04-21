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

@app.route("/get_friends/<string:dir_id>", methods=["GET"])
def get_friends(dir_id):
    friends = []
    student = Student.query.get(dir_id)
    student_data = {key: value for key, value in student.__dict__.items() if key.startswith('course') and value != None}
    for row in Student.query.all():
        if getattr(row, "dir_id") == dir_id:
            continue
        for course in student_data:
            if course in (getattr(row, column.name) for column in Student.__table__.columns):
                friends.append([getattr(row, "dir_id"), course])
    
    json_data = json.dumps(friends)
    return json_data



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

def update_courses(dir_id, courseList):
    student = Student.query.get(dir_id)

    if len(courseList) > 8:
        return jsonify({"message": "failed to update course list"}, 417)

    for i, course in enumerate(courseList):
        setattr(student, f"course{i + 1}", course)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
