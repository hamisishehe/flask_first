from functools import wraps
import datetime
from flask import Flask, request, jsonify
import jwt
from models import Role, User, db
import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import Instructor  
from models import Students
from models import Course
from models import Course_matrix

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

        print("✅ Instructors fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching instructors:", str(e))
        return jsonify({'message': 'Error fetching instructors', 'error': str(e)}), 500


@app.route('/add_student_program', methods=['POST'])
def add_Student():
    try:
        data = request.get_json()
        print("✅ JSON received:", data)

        programme = data.get('programme')
        total_students = data.get('total_students')
        coordinator_id = data.get('coordinator_id')

      

        if not all([programme, total_students,  coordinator_id]):
            print("❌ Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if Student program  already exists
        existing = Students.query.filter((Students.programme == programme)).first()
        if existing:
            print("❌ Program already exists")
            return jsonify({'message': 'Students with this Program  already exists'}), 409

        # ✅ Try saving
        new_Student = Students(
            programme = programme,
            total_students = total_students,
            coordinator_id=coordinator_id
        )

        db.session.add(new_Student)
        db.session.commit()
        print("✅ Student Program saved")

        return jsonify({'message': 'Student Program added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print("🔥 Exception occurred:", str(e))
        return jsonify({'message': 'Error while adding Student', 'error': str(e)}), 500

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
        existing = Course.query.filter((Students.course_code == course_code)).first()
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


@app.route('/assign-course', methods=['POST'])
def assign_Course():
    try:
        data = request.get_json()
        print("✅ JSON received:", data)


        instructor_id = data.get('instructor_id')
        course_id = data.get('course_id')
        student_id = data.get('student_id')
 

        if not all([course_id,instructor_id,student_id]):
            print("❌ Missing required fields")
            return jsonify({'message': 'Missing required fields'}), 400

        # Optional: check if Course  already assigned
        existing = Course_matrix.query.filter((Course_matrix.course_id == course_id)).first()
        if existing:
            print("❌ Course already Asigned")
            return jsonify({'message': 'Course already Asigned'}), 409

        # ✅ Try saving
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

@app.route('/assigned_course_list', methods=['GET'])
def get_assigned_course_list():
    try:
        course = Course.query.all()
        result = []

        course_matrix_entries = db.session.query(Course_matrix).all()

        for entry in course_matrix_entries:
            course = Course.query.get(entry.course_id)
            student = Students.query.get(entry.student_id)
            instructor = Instructor.query.get(entry.instructor_id)


            result = {
                "course": {
                    "id": course.id,
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "semester": course.semester,
                    "is_tutorial": course.is_tutorial,
                    "is_lecture": course.is_lecture,
                    "time_difference": course.time_difference
                },
                "student": {
                    "id": student.id,
                    "programme": student.programme,
                    "total_students": student.total_students
                },
                "instructor": {
                    "id": instructor.id,
                    "first_name": instructor.first_name,
                    "middle_name": instructor.middle_name,
                    "last_name": instructor.last_name,
                    "email": instructor.email,
                    "phone_number": instructor.phone_number,
                    "title": instructor.title
                }
            }    
     
            result.append(result)

        print("✅ course fetched:", result)
        return jsonify(result), 200

    except Exception as e:
        print("🔥 Error fetching course:", str(e))
        return jsonify({'message': 'Error fetching course', 'error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
