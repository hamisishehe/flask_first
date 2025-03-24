from functools import wraps
import datetime
from flask import Flask, request, jsonify
import jwt
from models import Role, User, db
import config
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route("/")
def index():
    return "hellow"





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
        "email": current_user.email,
        "role": current_user.role.name  # User role
    }

    return jsonify({"profile": profile_data}), 200


if __name__ == "__main__":
    app.run(debug=True)
