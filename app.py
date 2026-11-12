
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Database Models

class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(
        db.Integer, db.ForeignKey("student.student_id"), nullable=False
    )
    ecourse_id = db.Column(
        db.Integer, db.ForeignKey("course.course_id"), nullable=False
    )


# Helper function for selected courses

def get_selected_course_ids():
    selected = request.form.getlist("courses")
    course_ids = []

    for value in selected:
        if value.startswith("course_"):
            try:
                course_ids.append(int(value.split("_")[1]))
            except ValueError:
                pass

    return course_ids


# Home page: display all students

@app.route("/")
def index():
    students = Student.query.order_by(Student.student_id).all()
    return render_template("index.html", students=students)


# Create student

@app.route("/student/create", methods=["GET", "POST"])
def create_student():
    courses = Course.query.order_by(Course.course_id).all()

    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        first_name = request.form.get("f_name", "").strip()
        last_name = request.form.get("l_name", "").strip()

        student = Student(
            roll_number=roll,
            first_name=first_name,
            last_name=last_name
        )

        try:
            db.session.add(student)
            db.session.flush()

            selected_ids = get_selected_course_ids()

            for course_id in selected_ids:
                course = db.session.get(Course, course_id)
                if course:
                    enrollment = Enrollment(
                        estudent_id=student.student_id,
                        ecourse_id=course.course_id
                    )
                    db.session.add(enrollment)

            db.session.commit()
            return redirect(url_for("index"))

        except IntegrityError:
            db.session.rollback()
            return render_template("exists.html"), 200

    return render_template("create.html", courses=courses)


# Student details

@app.route("/student/<int:student_id>")
def student_details(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return "Student not found", 404

    enrollments = (
        db.session.query(Enrollment, Course)
        .join(Course, Enrollment.ecourse_id == Course.course_id)
        .filter(Enrollment.estudent_id == student_id)
        .order_by(Course.course_id)
        .all()
    )

    return render_template(
        "details.html",
        student=student,
        enrollments=enrollments
    )


# Update student

@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return "Student not found", 404

    courses = Course.query.order_by(Course.course_id).all()

    if request.method == "POST":
        student.first_name = request.form.get("f_name", "").strip()
        student.last_name = request.form.get("l_name", "").strip()

        Enrollment.query.filter_by(estudent_id=student_id).delete()

        selected_ids = get_selected_course_ids()

        for course_id in selected_ids:
            course = db.session.get(Course, course_id)
            if course:
                enrollment = Enrollment(
                    estudent_id=student_id,
                    ecourse_id=course.course_id
                )
                db.session.add(enrollment)

        db.session.commit()
        return redirect(url_for("index"))

    existing_ids = [
        enrollment.ecourse_id
        for enrollment in Enrollment.query.filter_by(
            estudent_id=student_id
        ).all()
    ]

    return render_template(
        "update.html",
        student=student,
        courses=courses,
        existing_ids=existing_ids
    )


# Delete student

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if student is not None:
        Enrollment.query.filter_by(estudent_id=student_id).delete()
        db.session.delete(student)
        db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
