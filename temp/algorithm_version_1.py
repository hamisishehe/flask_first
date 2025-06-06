from app import app
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix



with app.app_context(): 
    venue = {v.name: v.teaching_capacity for v in Venue.query.all()}
    student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}

    course_group_mapping = {}
    matrix_entries = Course_matrix.query.all()
    for entry in matrix_entries:
        course_name = entry.course.course_name
        programme = entry.student.programme
        course_group_mapping.setdefault(course_name, [])
        if programme not in course_group_mapping[course_name]:
            course_group_mapping[course_name].append(programme)

    course_instructor_mapping = {}
    for entry in matrix_entries:
        course_name = entry.course.course_name
        instructor = entry.instructor
        full_name = f"{instructor.first_name} {instructor.middle_name + ' ' if instructor.middle_name else ''}{instructor.last_name or ''}".strip()
        title = instructor.title or "Mr./Ms."
        instructor_display = f"{title}. {full_name}"
        course_instructor_mapping[course_name] = instructor_display

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    start_time = datetime.strptime("07:30", "%H:%M")
    timeslots = [(start_time + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
                 (start_time + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(5)]

    # Include tutorial timeslots (1 hour slots in afternoon)
    tutorial_start = datetime.strptime("13:30", "%H:%M")
    tutorial_slots = [(tutorial_start + timedelta(hours=i)).strftime("%H:%M") + "-" +
                      (tutorial_start + timedelta(hours=i + 1)).strftime("%H:%M") for i in range(3)]

    lecture_domains = {}
    tutorial_domains = {}
    for cls, groups in course_group_mapping.items():
        try:
            total_students = sum(student_groups[group] for group in groups)
        except KeyError:
            continue

        valid_lecture_slots = [
            (day, slot, room)
            for day in days
            for slot in timeslots
            for room in venue
            if venue[room] >= total_students
        ]
        if valid_lecture_slots:
            lecture_domains[cls] = valid_lecture_slots

        valid_tutorial_slots = [
            (day, slot, room)
            for day in days
            for slot in tutorial_slots
            for room in venue
            if venue[room] >= total_students
        ]
        if valid_tutorial_slots:
            tutorial_domains[cls + " (Tutorial)"] = valid_tutorial_slots

    all_courses = list(lecture_domains.keys()) + list(tutorial_domains.keys())

    def backtrack(schedule, prof_schedule, student_group_schedule):
        if len(schedule) == len(all_courses):
            return schedule, prof_schedule

        unassigned_class = next(cls for cls in all_courses if cls not in schedule)

        domains = lecture_domains if "Tutorial" not in unassigned_class else tutorial_domains
        for value in domains[unassigned_class]:
            day, time, room = value
            course_name = unassigned_class.replace(" (Tutorial)", "")
            professor = course_instructor_mapping.get(course_name)
            groups = course_group_mapping.get(course_name, [])

            conflict = False
            for existing_cls, (p_day, p_time, p_room) in schedule.items():
                if p_day == day and p_time == time:
                    if prof_schedule.get(existing_cls) == professor or p_room == room:
                        conflict = True
                        break

            for group in groups:
                if (day, time) in student_group_schedule.get(group, set()):
                    conflict = True
                    break

                # Add rest gap for lecture sessions only
                if "Tutorial" not in unassigned_class:
                    idx = timeslots.index(time) if time in timeslots else -1
                    if idx > 0 and (day, timeslots[idx - 1]) in student_group_schedule.get(group, set()):
                        conflict = True
                        break
                    if idx < len(timeslots) - 1 and (day, timeslots[idx + 1]) in student_group_schedule.get(group, set()):
                        conflict = True
                        break

            if conflict:
                continue

            schedule[unassigned_class] = (day, time, room)
            prof_schedule[unassigned_class] = professor
            for group in groups:
                student_group_schedule.setdefault(group, set()).add((day, time))

            result_schedule, result_profs = backtrack(schedule, prof_schedule, student_group_schedule)
            if result_schedule:
                return result_schedule, result_profs

            del schedule[unassigned_class]
            del prof_schedule[unassigned_class]
            for group in groups:
                student_group_schedule[group].remove((day, time))

        return None, None

    schedule = {}
    prof_schedule = {}
    student_group_schedule = {}
    solution, instructor_assignments = backtrack(schedule, prof_schedule, student_group_schedule)

    if solution:
        # Generate PDF only
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.set_font("helvetica", style='B', size=14)
        pdf.cell(0, 10, text="University Timetable (Monday to Friday)", ln=True, align='C')
        pdf.ln(5)

        headers = ["Day", "Time", "Course", "Student Groups", "Instructor", "Venue"]
        col_widths = [30, 30, 60, 60, 60, 40]
        pdf.set_font("helvetica", style='B', size=12)
        pdf.set_fill_color(200, 220, 255)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_font("helvetica", size=11)
        sorted_schedule = sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1]))

        for cls, (day, time, room) in sorted_schedule:
            course_name = cls.replace(" (Tutorial)", "")
            row_data = [day, time, cls, ", ".join(course_group_mapping[course_name]), instructor_assignments[cls], room]
            for i, item in enumerate(row_data):
                pdf.cell(col_widths[i], 10, item, border=1)
            pdf.ln()

        output_path = "static/timetable.pdf"
        pdf.output(output_path)
        print("✅ Timetable generated and saved successfully.")
    else:
        print("❌ No valid timetable could be generated.")
