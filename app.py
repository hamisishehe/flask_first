from functools import wraps
import datetime
import pandas as pd
import os
from flask import Flask, json, request, jsonify, send_file, send_from_directory, url_for
import jwt
from flask import session
from exam_api import generate_exam_timetable
from models import Department, Role, User, VenueType, db
import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import Instructor
from models import Students
from models import Course
from models import Course_matrix
from models import CourseMatrixView
from models import Venue
from models import Collage
from algorithm_api import generate_timetable
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config)


app.config["SECRET_KEY"] = "your-secret-key"


db.init_app(app)
migrate = Migrate(app, db)


# Decorator to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Check if the token is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # Bearer <Token>

        if not token:
            return jsonify({"error": "Token is missing"}), 403

        try:
            # Decode the token
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.get(
                data["sub"]
            )  # Get user by ID (sub is user ID)
            if not current_user:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 403

        # Add the user to the request context
        return f(current_user, *args, **kwargs)

    return decorated_function


CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return ""


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validate required fields
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": str(user.id),  # user ID
        "role": user.role.name,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=1),  # token expires in 1 hour
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token, "role": user.role.name}), 200


@app.route("/user/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    # Assuming the User model has these attributes: id, email, username, role
    profile_data = {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "middle_name": current_user.middle_name,
        "last_name": current_user.last_name,
        "phone_number": current_user.phone_number,
        "email": current_user.email,
        "department": current_user.department,
        "role": current_user.role.name,  # User role
    }

    return jsonify(profile_data), 200


@app.route("/add_collage", methods=["POST"])
def add_collage():
    data = request.get_json()
    name = data.get("name")
    short_name = data.get("short_name")

    if not all([name, short_name]):
        return jsonify({"error": "All fields are required"}), 400

    collage = Collage(name=name, short_name=short_name, description=short_name)
    db.session.add(collage)
    db.session.commit()

    return (
        jsonify({"message": "Collage added successfully", "collage_id": collage.id}),
        201,
    )


@app.route("/collages", methods=["GET"])
def get_collages():
    collages = Collage.query.all()
    result = []

    for collage in collages:
        result.append(
            {
                "id": collage.id,
                "name": collage.name,
                "short_name": collage.short_name,
            }
        )

    return jsonify(result), 200


@app.route("/add_venue", methods=["POST"])
def add_venue():
    data = request.get_json()

    name = data.get("name")
    location = data.get("location")
    exam_capacity = data.get("exam_capacity")
    teaching_capacity = data.get("teaching_capacity")
    venue_type = data.get("type")

    if not all([name, location, exam_capacity, teaching_capacity, venue_type]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        venue_enum = VenueType[venue_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid venue type"}), 400

    venue = Venue(
        name=name,
        location=location,
        exam_capacity=int(exam_capacity),
        teaching_capacity=int(teaching_capacity),
        type=venue_enum,
    )
    db.session.add(venue)
    db.session.commit()

    return jsonify({"message": "Venue added successfully", "venue_id": venue.id}), 201


@app.route("/venues", methods=["GET"])
def get_venues():
    venues = Venue.query.all()
    result = []

    for venue in venues:
        result.append(
            {
                "id": venue.id,
                "name": venue.name,
                "location": venue.location,
                "exam_capacity": venue.exam_capacity,
                "teaching_capacity": venue.teaching_capacity,
                "type": venue.type.name,
            }
        )

    return jsonify(result), 200


@app.route("/update_venue/<int:venue_id>", methods=["PUT"])
def update_venue(venue_id):
    data = request.get_json()

    name = data.get("name")
    location = data.get("location")
    exam_capacity = data.get("exam_capacity")
    teaching_capacity = data.get("teaching_capacity")
    venue_type = data.get("type")

    if not all([name, location, exam_capacity, teaching_capacity, venue_type]):
        return jsonify({"error": "All fields are required"}), 400

    venue = Venue.query.get(venue_id)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404

    try:
        venue_enum = VenueType[venue_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid venue type"}), 400

    venue.name = name
    venue.location = location
    venue.exam_capacity = int(exam_capacity)
    venue.teaching_capacity = int(teaching_capacity)
    venue.type = venue_enum

    db.session.commit()

    return jsonify({"message": "Venue updated successfully"})


@app.route("/add_departments", methods=["POST"])
def add_department():
    data = request.get_json()
    try:
        new_department = Department(
            name=data["name"],
            short_name=data["short_name"],
            description=data["short_name"],
            collage_id=data["collage_id"],
        )
        db.session.add(new_department)
        db.session.commit()
        return jsonify({"message": "Department added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/departments", methods=["GET"])
def get_departments():
    departments = Department.query.all()
    result = []

    for dept in departments:
        result.append(
            {
                "id": dept.id,
                "name": dept.name,
                "short_name": dept.short_name,
                "description": dept.description,
                "collage": {
                    "id": dept.collage.id,
                    "name": dept.collage.name,
                    "short_name": dept.collage.short_name,
                    "description": dept.collage.description,
                },
            }
        )

    return jsonify(result), 200


@app.route("/add_instructor", methods=["POST"])
def add_instructor():
    data = request.get_json()

    first_name = data.get("first_name")
    middle_name = data.get("middle_name")
    last_name = data.get("last_name")
    gender = data.get("gender")
    phone_number = data.get("phone_number")
    email = data.get("email")
    title = data.get("title")
    coordinator_id = data.get("coordinator_id")
    department_id = data.get("department_id")

    if not all([first_name, gender, email, title, coordinator_id, department_id]):
        return jsonify({"error": "Missing required fields"}), 400

    existing = Instructor.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Instructor with this email already exists"}), 409

    instructor = Instructor(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        gender=gender,
        phone_number=phone_number,
        email=email,
        title=title,
        coordinator_id=coordinator_id,
        department_id=department_id,
    )

    db.session.add(instructor)
    db.session.commit()

    return (
        jsonify(
            {"message": "Instructor added successfully", "instructor_id": instructor.id}
        ),
        201,
    )


@app.route("/instructors", methods=["GET"])
def get_instructors_full_info():
    instructors = Instructor.query.join(Department).join(Collage).all()
    result = []

    for inst in instructors:
        department = inst.department
        collage = department.collage  # because of backref='collage'

        result.append(
            {
                "id": inst.id,
                "first_name": inst.first_name,
                "middle_name": inst.middle_name,
                "last_name": inst.last_name,
                "gender": inst.gender,
                "phone_number": inst.phone_number,
                "email": inst.email,
                "title": inst.title,
                "coordinator_id": inst.coordinator_id,
                "department": {
                    "id": department.id,
                    "name": department.name,
                    "short_name": department.short_name,
                    "description": department.description,
                },
                "collage": {
                    "id": collage.id,
                    "name": collage.name,
                    "short_name": collage.short_name,
                    "description": collage.description,
                },
            }
        )

    return jsonify(result), 200


@app.route("/add_student_program", methods=["POST"])
def add_student():
    try:
        data = request.get_json()
        print("JSON received:", data)

        programme = data.get("programme")
        programme_code = data.get("programme_code")
        duration = data.get("duration")
        department_id = data.get("department_id")
        coordinator_id = data.get("coordinator_id")

        if not all(
            [programme, programme_code, duration, coordinator_id, department_id]
        ):
            print("Missing required fields")
            return jsonify({"message": "Missing required fields"}), 400

        # Optional: check if Student program already exists
        existing = Students.query.filter(
            Students.programme == programme, Students.department_id == department_id
        ).first()
        if existing:
            print("Program already exists")
            return jsonify({"message": "Student program already exists"}), 409

        # Insert multiple records based on duration
        for i in range(1, int(duration) + 1):
            new_code = f"{programme_code}{i}"  # e.g., SE1, SE2, SE3
            new_student = Students(
                programme=programme,
                programme_code=new_code,
                coordinator_id=coordinator_id,
                department_id=department_id,
            )
            db.session.add(new_student)

        db.session.commit()
        print("Student program(s) saved")

        return (
            jsonify({"message": f"{duration} Student Program(s) added successfully"}),
            201,
        )

    except Exception as e:
        db.session.rollback()
        print("Exception occurred:", str(e))
        return jsonify({"message": "Error while adding Student", "error": str(e)}), 500


@app.route("/upload-students", methods=["POST"])
def upload_students():

    coordinator_id = 1

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith((".xlsx", ".xls")):
        return (
            jsonify({"error": "Invalid file format. Please upload an Excel file."}),
            400,
        )

    try:
        df = pd.read_excel(file)

        required_columns = ["programme", "total_students"]
        if not all(col in df.columns for col in required_columns):
            return (
                jsonify(
                    {"error": f"Missing required columns. Required: {required_columns}"}
                ),
                400,
            )

        inserted = 0
        skipped = []

        for _, row in df.iterrows():
            existing = Students.query.filter_by(programme=row["programme"]).first()
            if existing:
                skipped.append(row["programme"])
                continue

            student = Students(
                programme=row["programme"],
                total_students=row["total_students"],
                coordinator_id=coordinator_id,
            )
            db.session.add(student)
            inserted += 1

        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"{inserted} students inserted successfully.",
                    "skipped_programmes": skipped,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/students", methods=["GET"])
def get_students():
    try:
        students = Students.query.all()
        result = []

        for stu in students:

            dept = stu.department

            students_data = {
                "id": stu.id,
                "programme": stu.programme,
                "programme_code": stu.programme_code,
                "total_students": stu.total_students,
                "department": (
                    {
                        "id": dept.id,
                        "name": dept.name,
                        "short_name": dept.short_name,
                        "description": dept.description,
                    }
                    if dept
                    else None
                ),
            }
            result.append(students_data)

        print("✅ Students fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching Students:", str(e))
        return jsonify({"message": "Error fetching Students", "error": str(e)}), 500


@app.route("/update_student_program/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        data = request.get_json()
        
        
        programme = data.get("programme")
        programme_code = data.get("programme_code")
        total_students = data.get("total_students")
     

        student = Students.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404

        # Update fields if provided
       
        student.programme = programme
        student.programme_code =programme_code
        student.total_students =total_students

        db.session.commit()
        return jsonify({"message": "Student program updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print("Exception:", str(e))
        return jsonify({"message": "Update failed", "error": str(e)}), 500


@app.route("/add_new_course", methods=["POST"])
def add_Course():
    try:
        data = request.get_json()
        print("✅ JSON received:", data)

        course_code = data.get("course_code")
        course_name = data.get("course_name")
        semester = data.get("semester")
        is_tutorial = data.get("is_tutorial")
        is_lecture = data.get("is_lecture")
        is_practical = data.get("is_practical")
        department_id = data.get("department_id")
        coordinator_id = data.get("coordinator_id")

        if not all(
            [
                course_code,
                course_name,
                semester,
                is_lecture,
                is_tutorial,
                department_id,
                coordinator_id,
            ]
        ):
            print("❌ Missing required fields")
            return jsonify({"message": "Missing required fields"}), 400

        # Optional: check if Course  already exists
        existing = Course.query.filter((Course.course_code == course_code)).first()
        if existing:
            print("❌ Course already exists")
            return jsonify({"message": "Course already exists"}), 409

        # ✅ Try saving
        new_Course = Course(
            course_code=course_code,
            course_name=course_name,
            semester=semester,
            is_tutorial=is_tutorial,
            is_lecture=is_lecture,
            is_practical=is_practical,
            coordinator_id=coordinator_id,
            department_id=department_id,
        )

        db.session.add(new_Course)
        db.session.commit()
        print("✅ Course Program saved")

        return jsonify({"message": "Course  added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print("🔥 Exception occurred:", str(e))
        return jsonify({"message": "Error while adding Course", "error": str(e)}), 500


@app.route("/course_list", methods=["GET"])
def get_course():
    try:
        courses = Course.query.all()
        result = []

        for cou in courses:
            # Get the related department object using SQLAlchemy relationship
            dept = cou.department  # thanks to backref="department" in Course model

            course_data = {
                "id": cou.id,
                "course_name": cou.course_name,
                "course_code": cou.course_code,
                "semester": cou.semester,
                "is_tutorial": cou.is_tutorial,
                "is_lecture": cou.is_lecture,
                "is_practical": cou.is_practical,
                "department": (
                    {
                        "id": dept.id,
                        "name": dept.name,
                        "short_name": dept.short_name,
                        "description": dept.description,
                    }
                    if dept
                    else None
                ),
            }

            result.append(course_data)

        print("✅ Courses with department fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching courses:", str(e))
        return jsonify({"message": "Error fetching courses", "error": str(e)}), 500


@app.route("/assign-course", methods=["POST"])
def assign_Course():
    try:
        data = request.get_json()
        print("JSON received:", data)

        instructor_id = data.get("instructor_id")
        course_id = data.get("course_id")
        student_ids = data.get("student_id")
        program_group= data.get("program_group")

        if not all([course_id, instructor_id, student_ids]):
            print("Missing required fields")
            return jsonify({"message": "Missing required fields"}), 400

        assigned = []
        skipped = []

        for student_id in student_ids:
            existing = Course_matrix.query.filter_by(
                course_id=course_id, student_id=student_id
            ).first()
            if existing:
                skipped.append(student_id)
                return (
                    jsonify(
                        {
                            "message": "Course Already Assigned",
                            "assigned": assigned,
                            "skipped": skipped,
                        }
                    ),
                    201,
                )

            new_assign_course = Course_matrix(
                instructor_id=instructor_id,
                course_id=course_id,
                student_id=student_id,
                program_group = program_group
            )
            db.session.add(new_assign_course)
            assigned.append(student_id)

        db.session.commit()
        print(f" Assigned to students: {assigned}")

        return (
            jsonify(
                {
                    "message": "Course assigned successfully",
                    "assigned": assigned,
                    "skipped": skipped,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        print(" Exception occurred:", str(e))
        return (
            jsonify({"message": "Error while assigning course", "error": str(e)}),
            500,
        )


@app.route("/view/course-matrix", methods=["GET"])
def get_course_matrix_view():
    results = CourseMatrixView.query.all()

    data = []
    for row in results:
        item = {
            "course_matrix_id": row.course_matrix_id,
            
            "course_matrix": {
                "program_group": row.program_group
            },
            
            "course": {
                "id": row.course_id,
                "name": row.course_name,
                "code": row.course_code,
                "semester": row.semester,
            },
            "instructor": {
                "id": row.instructor_id,
                "name": f"{row.instructor_first_name or ''} {row.instructor_last_name or ''}".strip(),
                "email": row.instructor_email,
                "title": row.instructor_title,
            },
            "student": {
                "id": row.student_id,
                "programme": row.programme,
                "programme_code": row.programme_code,
                "total_students": row.total_students,
            },
        }
        data.append(item)

    return jsonify(data)



@app.route('/timetable_semester_<int:semester>.json')
def serve_timetable(semester):
    return send_from_directory('.', f'timetable_semester_{semester}.json')

@app.route("/api/fetch-timetable-json", methods=["GET"])
def fetch_timetable_json():
    try:
        filename = os.path.join("saved_files", "timetable.json")

        with open(filename, "r") as f:
            data = json.load(f)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"message": str(e), "status": "error", "data": []}), 500


@app.route("/api/update-timetable-json", methods=["POST"])
def update_timetable_json():
    try:
        data = request.get_json()
        filename = os.path.join("saved_files", "timetable.json")
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Timetable updated successfully", "status": "success"}), 200
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    

@app.route("/api/generate-timetable", methods=["POST"])
def generate_timetable_route():
    try:
        data = request.get_json()

        start_time = data.get("start_time")
        semester = int(data.get("semester"))
   
        timetable = generate_timetable(app,semester,start_time)

        return (
            jsonify(
                {
                    "message": "Timetable generated successfully.",
                    "status": "success",
                    "data": timetable,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/api/save-timetable-json", methods=["POST"])
def save_timetable_json():
    try:

        data = request.get_json()

        save_folder = "saved_files"
        os.makedirs(save_folder, exist_ok=True)
        filename = os.path.join(save_folder, "timetable.json")

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return (
            jsonify(
                {
                    "message": "Timetable saved successfully as JSON.",
                    "status": "success",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/generate_exam_timetable", methods=["GET"])
def generate_exam_timetable_route():
    timetable = generate_exam_timetable()
    if timetable:
        return jsonify(
            timetable
        )  # Return the timetable as a sorted list of dictionaries
    else:
        return (
            jsonify({"error": "Could not generate timetable"}),
            500,
        )  # Return error if no timetable generated


@app.route("/api/last-timetable", methods=["GET"])
def get_last_timetable():
    try:

        with open("last_timetable.json", "r") as json_file:
            timetable = json.load(json_file)

        return (
            jsonify(
                {
                    "message": "Fetched last generated timetable.",
                    "status": "success",
                    "data": timetable,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/download-timetable")
def download_timetable():
    return send_file("static/timetable.pdf", as_attachment=True)


# ADD USERS
@app.route("/add_user", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        user = User(
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            phone_number=data["phone_number"],
            email=data["email"],
            department=data.get("department"),
            role=Role[data.get("role", "COORDINATOR").upper()],
        )
        user.set_password(data["first_name"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ All Users
@app.route("/view_users", methods=["GET"])
def get_users():
    users = User.query.all()
    return (
        jsonify(
            [
                {
                    "id": u.id,
                    "first_name": u.first_name,
                    "middle_name": u.middle_name,
                    "last_name": u.last_name,
                    "phone_number": u.phone_number,
                    "email": u.email,
                    "department": u.department,
                    "role": u.role.name,
                }
                for u in users
            ]
        ),
        200,
    )


# READ Single User by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return (
        jsonify(
            {
                "id": user.id,
                "first_name": user.first_name,
                "middle_name": user.middle_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "email": user.email,
                "department": user.department,
                "role": user.role.name,
            }
        ),
        200,
    )


# UPDATE User
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    try:
        user.first_name = data.get("first_name", user.first_name)
        user.middle_name = data.get("middle_name", user.middle_name)
        user.last_name = data.get("last_name", user.last_name)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.email = data.get("email", user.email)
        user.department = data.get("department", user.department)
        if "role" in data:
            user.role = Role[data["role"].upper()]
        if "password" in data:
            user.set_password(data["password"])

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE User
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
