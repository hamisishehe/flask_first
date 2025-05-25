from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

db = SQLAlchemy()


class Role(Enum):
    COORDINATOR = "coordinator"
    ADMIN = "admin"
    TIMETABLEMASTER = "timetablemaster"


class VenueType(Enum):
    LAB = "LAB"
    CLASS = "CLASS"


# Association Tables
student_course = db.Table(
    'student_course',
    db.Column('id', db.Integer, primary_key=True),  # Added ID
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

instructor_course = db.Table(
    'instructor_course',
    db.Column('id', db.Integer, primary_key=True),  # Added ID
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('priority', db.Integer, nullable=False)
)

class CourseMatrixView(db.Model):
    __tablename__ = 'course_matrix_view'
    __table_args__ = {'extend_existing': True}

    course_matrix_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    course_name = db.Column(db.String(100))
    course_code = db.Column(db.String(100))
    semester = db.Column(db.Integer)

    instructor_id = db.Column(db.Integer)
    instructor_first_name = db.Column(db.String(100))
    instructor_last_name = db.Column(db.String(100))
    instructor_email = db.Column(db.String(100))
    instructor_title = db.Column(db.String(100))

    student_id = db.Column(db.Integer)
    programme = db.Column(db.String(100))
    programme_code = db.Column(db.String(100))
    total_students = db.Column(db.String(100))

class Course_matrix(db.Model):
    __tablename__ = 'course_matrix'

    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    instructor = db.relationship('Instructor', backref='course_matrices')
    course = db.relationship('Course', backref='course_matrices')
    student = db.relationship('Students', backref='course_matrices')


class Course(db.Model):
    __tablename__ = "course"
    
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    is_tutorial = db.Column(db.Boolean, nullable=False)
    is_lecture = db.Column(db.Boolean, nullable=False)
    is_practical = db.Column(db.Boolean, nullable=False)
    

    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # New FK to coordinator

    students = db.relationship('Students', secondary=student_course, backref='courses')
    instructors = db.relationship('Instructor', secondary=instructor_course, backref='courses')

    def __repr__(self):
        return f"<Course {self.course_code}, Semester {self.semester}>"


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    programme = db.Column(db.String(100), nullable=False)
    programme_code = db.Column(db.String(100), nullable=False)
    total_students = db.Column(db.String(10))

    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Student {self.id}, Programme {self.programme}>"


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)

    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    

    def __repr__(self):
        return f"<Instructor {self.first_name} {self.last_name}, Title {self.title}>"

class Collage(db.Model):
    __tablename__ = 'collage' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # One-to-many relationship
    departments = db.relationship('Department', backref='collage', lazy=True)

    def __repr__(self):
        return f"<name {self.name}, description {self.description}>"

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    
  
    collage_id = db.Column(db.Integer, db.ForeignKey('collage.id'), nullable=False)
    
    
    instructors = db.relationship('Instructor', backref='department', lazy=True)
    
  
    def __repr__(self):
        return f"<name {self.name}, description {self.description}>"
    
      
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    exam_capacity = db.Column(db.Integer, nullable=False)
    teaching_capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(VenueType), nullable=False, default=VenueType.CLASS)
    def __repr__(self):
        return f"<Venue {self.name}, Location {self.location}>"


class ScheduledClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    student_groups = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)

 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.COORDINATOR)

    # Relationships
    students = db.relationship('Students', backref='coordinator', lazy=True)
    instructors = db.relationship('Instructor', backref='coordinator', lazy=True)
    courses = db.relationship('Course', backref='coordinator', lazy=True)  # Added relationship

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}, Role {self.role.name}>"

