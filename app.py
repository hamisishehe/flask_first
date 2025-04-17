from functools import wraps
import datetime
from flask import Flask, request, jsonify
import jwt
from models import Role, User, db
import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import Instructor  

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




if __name__ == "__main__":
    app.run(debug=True)
