from app import app
from fpdf import FPDF, XPos, YPos
from datetime import datetime, timedelta
import random
from models import db, Course, Students, Venue, Instructor, Course_matrix

# ========== Fetch all required data within app context ==========

with app.app_context():
    # Fetch all venues with their capacities
    venue = {
        v.name: v.teaching_capacity
        for v in Venue.query.all()
    }

    # Fetch all student groups with total students
    student_groups = {
        student.programme: int(student.total_students)
        for student in Students.query.all()
    }

    # Build course -> student group mapping
    course_group_mapping = {}
    matrix_entries = Course_matrix.query.all()

    for entry in matrix_entries:
        course_name = entry.course.course_name
        programme = entry.student.programme

        if course_name not in course_group_mapping:
            course_group_mapping[course_name] = []

        if programme not in course_group_mapping[course_name]:
            course_group_mapping[course_name].append(programme)

    # Define courses only from mapping (not all courses)
    course = list(course_group_mapping.keys())

    # Build course -> instructor mapping
    course_instructor_mapping = {}
    for entry in matrix_entries:
        course_name = entry.course.course_name
        instructor = entry.instructor

        full_name = f"{instructor.first_name} {instructor.middle_name + ' ' if instructor.middle_name else ''}{instructor.last_name or ''}".strip()
        instructor_display = f"{instructor.title}. {full_name}"

        if course_name not in course_instructor_mapping:
            course_instructor_mapping[course_name] = instructor_display

# ========== Define constants ==========

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
start_time = datetime.strptime("07:30", "%H:%M")
timeslots = [(start_time + timedelta(hours=2*i)).strftime("%H:%M") + "-" +
             (start_time + timedelta(hours=2*(i+1))).strftime("%H:%M") for i in range(5)]

# ========== Generate Domains with Room Capacity Constraints ==========

domains = {
    cls: [
        (day, slot, room) for day in days for slot in timeslots
        for room in venue if venue[room] >= max(student_groups[group] for group in course_group_mapping[cls])
    ]
    for cls in course
}

# ========== Constraint Functions ==========

def no_conflict(schedule):
    scheduled = [(val[0], val[1]) for val in schedule.values()]
    return len(scheduled) == len(set(scheduled))

def room_availability(schedule):
    day_time_room = [(val[0], val[1], val[2]) for val in schedule.values()]
    return len(day_time_room) == len(set(day_time_room))

def professor_availability(schedule, prof_schedule):
    prof_times = [(prof, val[0], val[1]) for prof, val in prof_schedule.items()]
    return len(prof_times) == len(set(prof_times))

# ========== Backtracking Algorithm ==========

def backtrack(schedule, domains, prof_schedule):
    if len(schedule) == len(course):
        if no_conflict(schedule) and room_availability(schedule) and professor_availability(schedule, prof_schedule):
            return schedule, prof_schedule
        return None, None

    unassigned_class = next(cls for cls in course if cls not in schedule)

    for value in domains[unassigned_class]:
        day, time, room = value
        professor = course_instructor_mapping[unassigned_class]

        if all(not (p_day == day and p_time == time)
               for p_cls, (p_day, p_time, _) in schedule.items()
               if prof_schedule.get(p_cls) == professor):
            
            schedule[unassigned_class] = (day, time, room)
            prof_schedule[unassigned_class] = professor

            if no_conflict(schedule) and room_availability(schedule) and professor_availability(schedule, prof_schedule):
                result_schedule, result_profs = backtrack(schedule, domains, prof_schedule)
                if result_schedule:
                    return result_schedule, result_profs

            del schedule[unassigned_class]
            del prof_schedule[unassigned_class]

    return None, None

# ========== Run Scheduler ==========

schedule = {}
prof_schedule = {}
solution, instructor_assignments = backtrack(schedule, domains, prof_schedule)

# ========== Generate PDF ==========


if solution:
    pdf = FPDF(orientation='L', unit='mm', format='A4')  # Landscape for better table space
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    # Title
    pdf.set_font("helvetica", style='B', size=14)
    pdf.cell(0, 10, text="University Timetable (Monday to Friday, 2-hour Sessions)", ln=True, align='C')
    pdf.ln(5)

    # Table header
    pdf.set_font("helvetica", style='B', size=12)
    pdf.set_fill_color(200, 220, 255)
    header = ["Day", "Time", "Course", "Student Groups", "Instructor", "Venue"]
    col_widths = [30, 30, 60, 60, 60, 40]

    for i, title in enumerate(header):
        pdf.cell(col_widths[i], 10, title, border=1, align='C', fill=True)
    pdf.ln()

    # Table content
    pdf.set_font("helvetica", size=11)
    for cls, (day, time, room) in sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1])):
        instructor = instructor_assignments.get(cls, "TBA")
        student_group_list = course_group_mapping.get(cls, [])
        student_groups_str = ", ".join(student_group_list)

        row = [day, time, cls, student_groups_str, instructor, room]

        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 10, item, border=1, align='L')
        pdf.ln()

    pdf.output("timetable.pdf")
    print("✅ Timetable generated and saved to 'timetable.pdf'")
else:
    print("❌ Failed to generate a valid schedule.")

