from functools import wraps
from datetime import datetime, timedelta
from fpdf import FPDF
import pandas as pd
import os
from flask import Flask, json, request, jsonify, send_file ,send_from_directory, url_for
import jwt
from flask import session 
from models import Role, User, db
import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import Instructor  
from models import Students
from models import Course
from models import Course_matrix
from models import CourseMatrixView
from models import Venue
from algorithm_api import generate_timetable





app = Flask(__name__)
app.config.from_object(config)


app.config['SECRET_KEY'] = 'your-secret-key'



db.init_app(app)


# Decorator to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Check if the token is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <Token>

        if not token:
            return jsonify({"error": "Token is missing"}), 403

        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data["sub"])  # Get user by ID (sub is user ID)
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


@app.route("/auth/registration", methods=["POST"])
def create_user():
    data = request.get_json()

    # Validate required fields
    required_fields = ["first_name", "last_name", "email", "password", "role", "phone_number"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Extract user data from request
    first_name = data["first_name"]
    middle_name = data.get("middle_name", "")  # Middle name is optional
    last_name = data["last_name"]
    phone_number = data["phone_number"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create new user
    new_user = User(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email,
        role=Role(role),  # Convert string to Enum
    )
    new_user.set_password(password)

    # Add user to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!", "user": {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "role": new_user.role.name,
    }}), 201


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
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # token expires in 1 hour
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "token": token,
        "role": user.role.name
    }), 200


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
        "role": current_user.role.name  # User role
    }

    return jsonify(profile_data), 200


@app.route('/venues', methods=['GET'])
def list_venues():
    venues = Venue.query.all()
    venue_list = [{
        "id": v.id,
        "name": v.name,
        "location": v.location,
        "exam_capacity": v.exam_capacity,
        "teaching_capacity": v.teaching_capacity,
        "type": v.type.name,
        "coordinator_id": v.coordinator_id
    } for v in venues]
    return jsonify(venue_list)


@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    try:
        data = request.get_json()
        print("✅ JSON received:", data)

        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        title = data.get('title')
        coordinator_id = data.get('coordinator_id')

        print("✅ Extracted values:")
        print(first_name, middle_name, last_name, phone_number, email, title, coordinator_id)

        if not all([first_name, last_name, phone_number, email, title, coordinator_id]):
            print("❌ Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if email or title already exists
        existing = Instructor.query.filter((Instructor.email == email)).first()
        if existing:
            print("❌ Instructor already exists")
            return jsonify({'message': 'Instructor with this email or title already exists'}), 409

        # ✅ Try saving
        new_instructor = Instructor(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            title=title,
            coordinator_id=coordinator_id
        )

        db.session.add(new_instructor)
        db.session.commit()
        print("✅ Instructor saved")

        return jsonify({'message': 'Instructor added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print("🔥 Exception occurred:", str(e))
        return jsonify({'message': 'Error while adding instructor', 'error': str(e)}), 500

@app.route('/instructors', methods=['GET'])
def get_instructors():
    try:
        instructors = Instructor.query.all()
        result = []

        for inst in instructors:
            instructor_data = {
                'id': inst.id,
                'first_name': inst.first_name,
                'middle_name': inst.middle_name,
                'last_name': inst.last_name,
                'email': inst.email,
                'phone_number': inst.phone_number,
                'title': inst.title,
            }
            result.append(instructor_data)

        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching instructors:", str(e))
        return jsonify({'message': 'Error fetching instructors', 'error': str(e)}), 500


@app.route('/add_student_program', methods=['POST'])
def add_Student():
    try:
        data = request.get_json()
        print(" JSON received:", data)

        programme = data.get('programme')
        total_students = data.get('total_students')
        coordinator_id = data.get('coordinator_id')

      

        if not all([programme, total_students,  coordinator_id]):
            print(" Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if Student program  already exists
        existing = Students.query.filter((Students.programme == programme)).first()
        if existing:
            print(" Program already exists")
            return jsonify({'message': 'Students with this Program  already exists'}), 409

        #  Try saving
        new_Student = Students(
            programme = programme,
            total_students = total_students,
            coordinator_id=coordinator_id
        )

        db.session.add(new_Student)
        db.session.commit()
        print(" Student Program saved")

        return jsonify({'message': 'Student Program added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print(" Exception occurred:", str(e))
        return jsonify({'message': 'Error while adding Student', 'error': str(e)}), 500


@app.route('/upload-students', methods=['POST'])
def upload_students():
    
    coordinator_id = 1

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Invalid file format. Please upload an Excel file.'}), 400

    try:
        df = pd.read_excel(file)

        required_columns = ['programme', 'total_students']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': f'Missing required columns. Required: {required_columns}'}), 400

        inserted = 0
        skipped = []

        for _, row in df.iterrows():
            existing = Students.query.filter_by(programme=row['programme']).first()
            if existing:
                skipped.append(row['programme'])
                continue

            student = Students(
                programme=row['programme'],
                total_students=row['total_students'],
                coordinator_id=coordinator_id 
            )
            db.session.add(student)
            inserted += 1

        db.session.commit()

        return jsonify({
            'message': f'{inserted} students inserted successfully.',
            'skipped_programmes': skipped
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students', methods=['GET'])
def get_students():
    try:
        students = Students.query.all()
        result = []

        for stu in students:
            students_data = {
                'id': stu.id,
                'programme': stu.programme,
                'total_students': stu.total_students,

            }
            result.append(students_data)

        print("✅ Students fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching Students:", str(e))
        return jsonify({'message': 'Error fetching Students', 'error': str(e)}), 500


@app.route('/add_new_course', methods=['POST'])
def add_Course():
    try:
        data = request.get_json()
        print("✅ JSON received:", data)


        course_code = data.get('course_code')
        course_name = data.get('course_name')
        semester = data.get('semester')
        is_tutorial = data.get('is_tutorial')
        is_lecture = data.get('is_lecture')
        time_difference = data.get('time_difference')
        coordinator_id = data.get('coordinator_id')

      

        if not all([course_code, course_name, semester, is_lecture, is_tutorial, time_difference,  coordinator_id]):
            print("❌ Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if Course  already exists
        existing = Course.query.filter((Course.course_code == course_code)).first()
        if existing:
            print("❌ Course already exists")
            return jsonify({'message': 'Course already exists'}), 409

        # ✅ Try saving
        new_Course = Course(
            course_code = course_code,
            course_name = course_name,
            semester = semester,
            is_tutorial = is_tutorial,
            is_lecture = is_lecture,
            time_difference = time_difference,
            coordinator_id = coordinator_id
        )

        db.session.add(new_Course)
        db.session.commit()
        print("✅ Course Program saved")

        return jsonify({'message': 'Course  added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print("🔥 Exception occurred:", str(e))
        return jsonify({'message': 'Error while adding Course', 'error': str(e)}), 500

@app.route('/course_list', methods=['GET'])
def get_course():
    try:
        course = Course.query.all()
        result = []


        for cou in course:
            course_data = {
                'id': cou.id,
                'course_name' : cou.course_name,
                'course_code' : cou.course_code,
                'semester' :cou.semester,
                'is_tutorial' : cou.is_tutorial,
                'is_lecture' : cou.is_lecture,
                'time_difference' : cou.time_difference,
            }
     
            result.append(course_data)

        print("✅ course fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching course:", str(e))
        return jsonify({'message': 'Error fetching course', 'error': str(e)}), 500



    try:
        data = request.get_json()
        print("JSON received:", data)

        instructor_id = data.get('instructor_id')
        course_id = data.get('course_id')
        student_ids = data.get('student_id')

        if not all([course_id, instructor_id, student_ids]):
            print("Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        assigned = []
        skipped = []

        for student_id in student_ids:
            existing = Course_matrix.query.filter_by(course_id=course_id, student_id=student_id).first()
            if existing:
                skipped.append(student_id)
                continue

            new_assign_course = Course_matrix(
                instructor_id=instructor_id,
                course_id=course_id,
                student_id=student_id,
            )
            db.session.add(new_assign_course)
            assigned.append(student_id)

        db.session.commit()
        print(f"Assigned to students: {assigned}")

        return jsonify({
            'message': 'Course assigned successfully',
            'assigned': assigned,
            'skipped': skipped
        }), 201

    except Exception as e:
        db.session.rollback()
        print("Exception occurred:", str(e))
        return jsonify({'message': 'Error while assigning course', 'error': str(e)}), 500

    try:
        data = request.get_json()
        print(" JSON received:", data)


        instructor_id = data.get('instructor_id')
        course_id = data.get('course_id')
        student_id = data.get('student_id')
 

        if not all([course_id,instructor_id,student_id]):
            print(" Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if Course and students already assigned
        existing = Course_matrix.query.filter_by(course_id=course_id, student_id=student_id).first()
        if existing:
            print("Course and students already Asigned")
            return jsonify({'message': 'Course already Asigned'}), 409

        # ✅Try saving
        new_assign_course = Course_matrix(
            instructor_id = instructor_id,
            course_id = course_id,
            student_id = student_id,
        )

        db.session.add(new_assign_course)
        db.session.commit()
        print("✅ Course  saved")

        return jsonify({'message': 'Course  added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print("🔥 Exception occurred:", str(e))
        return jsonify({'message': 'Error while adding Course', 'error': str(e)}), 500

@app.route('/assign-course', methods=['POST'])
def assign_Course():
    try:
        data = request.get_json()
        print("JSON received:", data)

        instructor_id = data.get('instructor_id')
        course_id = data.get('course_id')
        student_ids = data.get('student_id')

        if not all([course_id, instructor_id, student_ids]):
            print("Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        assigned = []
        skipped = []

        for student_id in student_ids:
            existing = Course_matrix.query.filter_by(course_id=course_id, student_id=student_id).first()
            if existing:
                skipped.append(student_id)
                return jsonify({
                    'message': 'Course Already Assigned',
                    'assigned': assigned,
                    'skipped': skipped
                 }), 201

            new_assign_course = Course_matrix(
                instructor_id=instructor_id,
                course_id=course_id,
                student_id=student_id,
            )
            db.session.add(new_assign_course)
            assigned.append(student_id)

        db.session.commit()
        print(f" Assigned to students: {assigned}")

        return jsonify({
            'message': 'Course assigned successfully',
            'assigned': assigned,
            'skipped': skipped
        }), 201

    except Exception as e:
        db.session.rollback()
        print(" Exception occurred:", str(e))
        return jsonify({'message': 'Error while assigning course', 'error': str(e)}), 500


@app.route('/view/course-matrix', methods=['GET'])
def get_course_matrix_view():
    results = CourseMatrixView.query.all()

    data = []
    for row in results:
        item = {
            "course_matrix_id": row.course_matrix_id,
            "course": {
                "id": row.course_id,
                "name": row.course_name,
                "code": row.course_code,
                "semester": row.semester,
            },
            "instructor": {
                "id": row.instructor_id,
                "name": f"{row.instructor_first_name} {row.instructor_last_name}",
                "email": row.instructor_email,
                "title": row.instructor_title,
            },
            "student": {
                "id": row.student_id,
                "programme": row.programme,
                "total_students": row.total_students
            }
        }
        data.append(item)

    return jsonify(data)


# @app.route('/generate-timetable', methods=['POST'])
# def generate_timetable_route():
#     try:
#         generate_timetable(app)
#         return jsonify({"message": "Timetable generated successfully.", "status": "success"}), 200
#     except Exception as e:
#         return jsonify({"message": str(e), "status": "error"}), 500

@app.route('/api/generate-timetable', methods=['POST'])
def generate_timetable_route():
    try:
        timetable = generate_timetable(app)
        return jsonify({
            "message": "Timetable generated successfully.",
            "status": "success",
            "data": timetable
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500
    

    
@app.route('/api/last-timetable', methods=['GET'])
def get_last_timetable():
    try:
        # Load the last generated timetable from the JSON file
        with open('last_timetable.json', 'r') as json_file:
            timetable = json.load(json_file)

        return jsonify({
            "message": "Fetched last generated timetable.",
            "status": "success",
            "data": timetable
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500

@app.route('/download-timetable')
def download_timetable():
    return send_file("static/timetable.pdf", as_attachment=True)





if __name__ == "__main__":
    app.run(debug=True)
