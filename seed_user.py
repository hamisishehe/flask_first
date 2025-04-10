from models import db, User, Role  
from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fyp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_user():
    with app.app_context():
        db.create_all() 

        if not User.query.filter_by(email='coordinator@example.com').first():
            user = User(
                first_name='coordinator',
                middle_name='A.',
                last_name='Doe',
                phone_number='0744982380',
                email='coordinator@example.com',
                role=Role.COORDINATOR
            )
            user.set_password('123456')

            db.session.add(user)
            db.session.commit()
            print("✅ User seeded successfully!")
        else:
            print("ℹ️ User already exists.")

if __name__ == '__main__':
    seed_user()
