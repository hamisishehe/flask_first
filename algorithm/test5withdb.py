from app import app
from fpdf import FPDF
from datetime import datetime, timedelta
import random
from models import db,Course, Students

# Fect all Course
with app.app_context():
    course = [c.course_name for c in Course.query.all()]
    print(course)

#fetch student group
with app.app_context():
    student_groups = {
        student.programme: int(student.total_students)
        for student in Students.query.all()
    }
    print(student_groups)

# class_group_mapping = {
#     'Math': ['ComputerEngineering', 'ElectricalEngineering'],
#     'Physics': ['ComputerEngineering', 'ElectricalEngineering'],
#     'Chemistry': ['ComputerEngineering'],
#     'Biology': ['ElectricalEngineering'],
#     'ComputerScience': ['ComputerEngineering'],
#     'English': ['BusinessStudies'],
#     'History': ['Law'],
#     'Geography': ['BusinessStudies'],
#     'Art': ['BusinessStudies'],
#     'Economics': ['BusinessStudies'],
#     'Philosophy': ['Law'],
#     'Statistics': ['ComputerEngineering'],
#     'Business': ['BusinessStudies'],
#     'Accounting': ['BusinessStudies'],
#     'Drama': ['BusinessStudies'],
#     'Sociology': ['Law'],
#     'Law': ['Law'],
#     'PoliticalScience': ['Law'],
#     'EnvironmentalScience': ['ElectricalEngineering'],
#     'Psychology': ['Law']
# }

# # Professors assigned to each class
# professors = [f"Prof_{chr(65+i)}" for i in range(20)]
# random.shuffle(professors)
# class_professor_mapping = dict(zip(classes, professors))

# # Rooms
# rooms = {
#     f"Room_{i+1}": cap for i, cap in enumerate([50, 60, 80, 100, 120, 90, 70, 110, 60, 100])
# }

# # Days and Time Slots
# days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
# start_time = datetime.strptime("08:00", "%H:%M")
# timeslots = [
#     (start_time + timedelta(hours=2*i)).strftime("%H:%M") + "-" +
#     (start_time + timedelta(hours=2*(i+1))).strftime("%H:%M")
#     for i in range(5)
# ]

# # Domain generation
# domains = {
#     cls: [
#         (day, slot, room) for day in days for slot in timeslots
#         for room in rooms if rooms[room] >= max(student_groups[group] for group in class_group_mapping[cls])
#     ]
#     for cls in classes
# }

# def is_valid(schedule, cls, val, prof, used_slots, used_rooms, used_profs):
#     day, time, room = val
#     if (day, time) in used_slots:
#         return False
#     if (day, time, room) in used_rooms:
#         return False
#     if (prof, day, time) in used_profs:
#         return False
#     return True

# def backtrack(schedule, used_slots, used_rooms, used_profs):
#     if len(schedule) == len(classes):
#         return schedule

#     unassigned = [cls for cls in classes if cls not in schedule]
#     random.shuffle(unassigned)

#     cls = unassigned[0]
#     prof = class_professor_mapping[cls]
#     domain_values = domains[cls]
#     random.shuffle(domain_values)

#     for val in domain_values:
#         if is_valid(schedule, cls, val, prof, used_slots, used_rooms, used_profs):
#             day, time, room = val
#             schedule[cls] = (day, time, room, prof)

#             used_slots.add((day, time))
#             used_rooms.add((day, time, room))
#             used_profs.add((prof, day, time))

#             result = backtrack(schedule, used_slots, used_rooms, used_profs)
#             if result:
#                 return result

#             del schedule[cls]
#             used_slots.remove((day, time))
#             used_rooms.remove((day, time, room))
#             used_profs.remove((prof, day, time))

#     return None

# # Generate schedule
# schedule = backtrack({}, set(), set(), set())

# # PDF generation
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=10)

# # Header
# pdf.set_font("Arial", 'B', size=12)
# pdf.cell(0, 10, "Class Schedule", ln=True, align='C')
# pdf.set_font("Arial", size=10)
# pdf.ln(5)
# pdf.set_fill_color(200, 220, 255)
# pdf.cell(30, 10, "Class", 1, 0, 'C', 1)
# pdf.cell(50, 10, "Groups", 1, 0, 'C', 1)
# pdf.cell(30, 10, "Professor", 1, 0, 'C', 1)
# pdf.cell(25, 10, "Day", 1, 0, 'C', 1)
# pdf.cell(35, 10, "Time", 1, 0, 'C', 1)
# pdf.cell(20, 10, "Room", 1, 1, 'C', 1)

# # Rows
# for cls in classes:
#     if cls in schedule:
#         day, time, room, prof = schedule[cls]
#         groups = ', '.join(class_group_mapping[cls])
#         pdf.cell(30, 10, cls, 1)
#         pdf.cell(50, 10, groups, 1)
#         pdf.cell(30, 10, prof, 1)
#         pdf.cell(25, 10, day, 1)
#         pdf.cell(35, 10, time, 1)
#         pdf.cell(20, 10, room, 1)
#         pdf.ln()

# # Save PDF
# pdf.output("class_schedule.pdf")

# print("Schedule PDF generated: class_schedule.pdf")
