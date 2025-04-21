from app import app
from fpdf import FPDF
from datetime import datetime, timedelta
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

    # Define courses only from mapping
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

# ========== Constants ==========

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
start_time = datetime.strptime("07:30", "%H:%M")
timeslots = [(start_time + timedelta(hours=2*i)).strftime("%H:%M") + "-" +
             (start_time + timedelta(hours=2*(i+1))).strftime("%H:%M") for i in range(5)]

# ========== Domains: Course -> List of (Day, Time, Room) Options ==========

domains = {
    cls: [
        (day, slot, room) for day in days for slot in timeslots
        for room in venue if venue[room] >= max(student_groups[group] for group in course_group_mapping[cls])
    ]
    for cls in course
}

# ========== Backtracking ==========

def backtrack(schedule, prof_schedule):
    if len(schedule) == len(course):
        return schedule, prof_schedule

    unassigned_class = next(cls for cls in course if cls not in schedule)

    for value in domains[unassigned_class]:
        day, time, room = value
        professor = course_instructor_mapping[unassigned_class]

        conflict = False
        for p_cls, (p_day, p_time, p_room) in schedule.items():
            if p_day == day and p_time == time:
                if prof_schedule.get(p_cls) == professor or p_room == room:
                    conflict = True
                    break

        if conflict:
            continue

        schedule[unassigned_class] = (day, time, room)
        prof_schedule[unassigned_class] = professor

        result_schedule, result_profs = backtrack(schedule, prof_schedule)
        if result_schedule:
            return result_schedule, result_profs

        del schedule[unassigned_class]
        del prof_schedule[unassigned_class]

    return None, None

# ========== Run Scheduling ==========

schedule = {}
prof_schedule = {}
solution, instructor_assignments = backtrack(schedule, prof_schedule)

# ========== Generate PDF ==========

if solution:
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    # Title
    pdf.set_font("helvetica", style='B', size=14)
    pdf.cell(0, 10, text="University Timetable (Monday to Friday, 2-hour Sessions)", ln=True, align='C')
    pdf.ln(5)

    # Table headers
    headers = ["Day", "Time", "Course", "Student Groups", "Instructor", "Venue"]
    col_widths = [30, 30, 60, 60, 60, 40]

    pdf.set_font("helvetica", style='B', size=12)
    pdf.set_fill_color(200, 220, 255)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
    pdf.ln()

    # Table content
    pdf.set_font("helvetica", size=11)

    # Sort solution by day and time for readability
    sorted_schedule = sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1]))

    for cls, (day, time, room) in sorted_schedule:
        student_group_list = ", ".join(course_group_mapping[cls])
        instructor = instructor_assignments[cls]

        row_data = [day, time, cls, student_group_list, instructor, room]

        for i, item in enumerate(row_data):
            pdf.cell(col_widths[i], 10, item, border=1)
        pdf.ln()

    # Output PDF
    pdf.output("timetable.pdf")
else:
    print("No valid timetable could be generated.")
