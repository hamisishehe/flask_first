from fpdf import FPDF
from app import app
from datetime import datetime, timedelta
from models import Course, Students, Venue, Course_matrix

def generate_exam_timetable():
    # Fetch venue and student data from the database
    venue = {v.name: v.exam_capacity for v in Venue.query.all()}  # Use exam_capacity
    student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}
    course_group_mapping = {}

    # Fetch matrix entries that link courses and student groups
    matrix_entries = Course_matrix.query.all()
    for entry in matrix_entries:
        course_code = entry.course.course_code
        programme = entry.student.programme
        course_group_mapping.setdefault(course_code, [])
        if programme not in course_group_mapping[course_code]:
            course_group_mapping[course_code].append(programme)

    # Set up week days and time slots
    start_date = datetime.strptime("2023-04-30", "%Y-%m-%d")  # Start date is 30th April 2023
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days = week_days * 4  # Expand to four weeks of Monday-Friday

    # Adjust exam timeslots to new schedule: 08:00-11:00, 11:30-14:30, 15:00-18:00
    exam_timeslots = [
        "08:00-11:00", 
        "11:30-14:30", 
        "15:00-18:00"
    ]
    
    # Setup domains for courses and available timeslots
    course_domains = {}
    for course_code, groups in course_group_mapping.items():
        try:
            total_students = sum(student_groups[group] for group in groups)
        except KeyError:
            continue

        valid_slots = [
            (day, timeslot, room)
            for day in days
            for timeslot in exam_timeslots
            for room, capacity in venue.items()
            if capacity >= total_students  # Ensure exam_capacity is used here
        ]
        if valid_slots:
            course_domains[course_code] = valid_slots

    all_courses = list(course_domains.keys())

    # Generate actual dates for the timetable
    def get_actual_date(week_num, day_name):
        # Calculate the actual date for the given week and day
        day_index = week_days.index(day_name)
        week_start = start_date + timedelta(weeks=week_num)
        actual_date = week_start + timedelta(days=day_index)
        return actual_date.strftime("%Y-%m-%d")

    # Backtracking function to generate a timetable with conflict prevention
    def backtrack(schedule, booked_timeslots, group_schedule):
        if len(schedule) == len(all_courses):
            return schedule

        unassigned_course = next(course for course in all_courses if course not in schedule)

        for day, timeslot, room in course_domains[unassigned_course]:
            groups = course_group_mapping.get(unassigned_course, [])
            conflict = False

            # Ensure no venue double-booking for the same timeslot
            if (day, timeslot, room) in booked_timeslots:
                continue  # Skip if the venue is already booked for the timeslot

            # Check capacity and student distribution
            try:
                total_students = sum(student_groups[group] for group in groups)
                capacity_ok = venue[room] >= total_students
                if not capacity_ok:
                    continue  # Skip if the room is not big enough for all students
            except KeyError:
                continue  # Skip if the student group is not found

            # Try assigning this course
            schedule[unassigned_course] = (day, timeslot, room, groups)  # Include groups in schedule
            booked_timeslots.add((day, timeslot, room))

            # Ensure each group has at least one exam on the same day
            try:
                group_schedule = assign_groups_to_day(schedule, group_schedule, groups, unassigned_course)
            except Exception:
                # If assignment fails, undo and continue
                del schedule[unassigned_course]
                booked_timeslots.remove((day, timeslot, room))
                continue

            result = backtrack(schedule, booked_timeslots, group_schedule)
            if result:
                return result

            # Undo the assignment if no solution found
            del schedule[unassigned_course]
            booked_timeslots.remove((day, timeslot, room))

        return None

    # Function to ensure each group gets at least one exam
    def assign_groups_to_day(schedule, group_schedule, groups, course_code):
        assigned_groups = set()
        for group in groups:
            assigned = False
            for day, timeslot, room in course_domains[course_code]:
                if (day, timeslot) not in group_schedule.get(group, set()):
                    group_schedule.setdefault(group, set()).add((day, timeslot))
                    assigned = True
                    break
            if not assigned:
                raise Exception(f"No valid exam time found for group {group} in course {course_code}")
        return group_schedule

    # Start the backtracking to find a valid schedule
    final_schedule = backtrack({}, set(), {})

    if not final_schedule:
        print("No valid exam timetable could be generated.")
        return None

    # Map the final schedule to actual dates for the first and second week
    final_schedule_with_dates = {}
    for course, (day, timeslot, room, groups) in final_schedule.items():
        week_num = 0 if day in week_days else 1  # First week or second week
        actual_date = get_actual_date(week_num, day)
        final_schedule_with_dates[course] = (actual_date, timeslot, room, groups)

    # Sort the final schedule by date
    sorted_schedule = dict(sorted(final_schedule_with_dates.items(), key=lambda item: datetime.strptime(item[1][0], "%Y-%m-%d")))

    # Generate the PDF report
    generate_pdf(sorted_schedule)

    return sorted_schedule

# Function to generate the PDF
def generate_pdf(timetable):
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add a page
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Exam Timetable", ln=True, align='C')

    # Set header font for table
    pdf.ln(10)  # Line break after the title
    pdf.set_font("Arial", 'B', 12)

    # Define table headers
    headers = ["Date", "Time", "Student Group", "Course Code", "Venue"]
    column_widths = [40, 40, 60, 40, 40]

    # Draw headers
    for i, header in enumerate(headers):
        pdf.cell(column_widths[i], 10, header, border=1, align='C')

    pdf.ln()  # Line break after headers

    # Set regular font for table rows
    pdf.set_font("Arial", size=10)

    # Fill in the table with the timetable data
    for course, schedule in timetable.items():
        date, time, room, groups = schedule
        student_groups = ', '.join(groups)

        # Output row data
        pdf.cell(column_widths[0], 10, date, border=1, align='C')
        pdf.cell(column_widths[1], 10, time, border=1, align='C')
        pdf.cell(column_widths[2], 10, student_groups, border=1, align='C')
        pdf.cell(column_widths[3], 10, course, border=1, align='C')
        pdf.cell(column_widths[4], 10, room, border=1, align='C')

        pdf.ln()  # Line break after each row

    # Save PDF to a file
    pdf_output_path = "exam_timetable.pdf"
    pdf.output(pdf_output_path)
    print(f"PDF generated successfully and saved to {pdf_output_path}")

# Wrap function call inside app context
if __name__ == "__main__":
    with app.app_context():
        timetable = generate_exam_timetable()
        if timetable:
            print("Generated Timetable:")
            for course, schedule in timetable.items():
                groups = ', '.join(schedule[3])  # Display student groups
                print(f"Course {course}: Date: {schedule[0]}, Time: {schedule[1]}, Room: {schedule[2]}, Student Groups: {groups}")
