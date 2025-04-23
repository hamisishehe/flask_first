from app import app, db
from models import Course
import itertools

# Fetch all courses from the database
courses = Course.query.all()

# Print the courses fetched from the database
print("Courses fetched from the database:")
for course in courses:
    print(f"Course Name: {course.course_name}, Course Code: {course.course_code}, Semester: {course.semester}")

# Time slots available for each day (2-hour sessions)
time_slots = [
    '07:30-09:30', '09:30-11:30', '11:30-13:30', '13:30-15:30', '15:30-17:30', '17:30-19:30'
]

# Days of the week
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Initialize a list to hold all CSP variables (time slots for each course)
csp_variables = []

# Generate CSP variables for each course
for course in courses:
    for day, time in itertools.product(days_of_week, time_slots):
        # Create variable name for each course (e.g., 'CS101_Monday_07:30-09:30')
        variable_name = f"{course.course_code}_{day}_{time}"
        csp_variables.append(variable_name)

# Print the generated CSP variables
print("\nGenerated CSP Variables:")
for var in csp_variables:
    print(var)
