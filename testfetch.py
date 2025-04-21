from app import app
from models import db, Course

with app.app_context():
    course = Course.query.all()
    for co in course:
        print(f"id: {co.id}, Username: {co.course_code}, name: {co.course_name}")
