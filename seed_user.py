from models import db, User, Role
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fyp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_users():
    with app.app_context():
        db.create_all()

        users = [
            {
                "first_name": "timetablemaster",
                "middle_name": "B.",
                "last_name": "timetablemaster",
                "phone_number": "0744982310",
                "email": "timetablemaster@udom.co.tz",
                "password": "Password123",
                "role": Role.TIMETABLEMASTER
            },
            {
                "first_name": "coordinator",
                "middle_name": "A.",
                "last_name": "coordinator",
                "phone_number": "1234567890",
                "email": "coordinator@udom.co.tz",
                "password": "Password123",
                "role": Role.COORDINATOR
            },
            {
                "first_name": "admin",
                "middle_name": None,
                "last_name": "admin",
                "phone_number": "0987654321",
                "email": "admin@udom.co.tz",
                "password": "securepass123",
                "role": Role.ADMIN
            }
        ]

        for user_data in users:
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if not existing_user:
                user = User(
                    first_name=user_data["first_name"],
                    middle_name=user_data["middle_name"],
                    last_name=user_data["last_name"],
                    phone_number=user_data["phone_number"],
                    email=user_data["email"],
                    role=user_data["role"]
                )
                user.set_password(user_data["password"])
                db.session.add(user)
                print(f"✔ {user.email} seeded successfully.")
            else:
                print(f"ℹ {user_data['email']} already exists.")

        db.session.commit()

if __name__ == '__main__':
    seed_users()
