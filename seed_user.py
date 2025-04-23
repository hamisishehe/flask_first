from models import db, User, Role  
from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fyp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def seed_user():
    with app.app_context():
        db.create_all() 

        if not User.query.filter_by(email='timetablemaster@example.com').first():
            user2 = User(
                first_name='timetablemaster',
                middle_name='B.',
                last_name='timetablemaster',
                phone_number='0744982310',
                email='timetablemaster@example.com',
                role=Role.TIMETABLEMASTER
            )
            user2.set_password('timetablemaster1234')
            db.session.add(user2)
            print(" timetablemaster user seeded successfully!")
        else:
            print("ℹ timetablemaster user already exists.")    

if __name__ == '__main__':
    seed_user()
