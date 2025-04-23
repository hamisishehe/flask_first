from app import app
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix, ScheduledClass


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
    lecture_timeslots = [(start_time + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
                         (start_time + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(5)]

    tutorial_start = datetime.strptime("12:30", "%H:%M")
    tutorial_timeslots = [(tutorial_start + timedelta(hours=i)).strftime("%H:%M") + "-" +
                          (tutorial_start + timedelta(hours=i + 1)).strftime("%H:%M") for i in range(3)]

    domains = {}
    for cls, groups in course_group_mapping.items():
        try:
            total_students = sum(student_groups[group] for group in groups)
        except KeyError:
            continue
        valid_slots = [
            (day, slot, room)
            for day in days
            for slot in lecture_timeslots
            for room in venue
            if venue[room] >= total_students
        ]
        tutorial_valid_slots = [
            (day, slot, room)
            for day in days
            for slot in tutorial_timeslots
            for room in venue
            if venue[room] >= total_students
        ]
        if valid_slots and tutorial_valid_slots:
            domains[cls] = {
                "lecture": valid_slots,
                "tutorial": tutorial_valid_slots
            }

    course = list(domains.keys())

    def backtrack(schedule, prof_schedule, student_group_schedule):
        if len(schedule) == len(course) * 2:
            return schedule, prof_schedule

        for cls in course:
            if (cls, "lecture") not in schedule:
                session_type = "lecture"
            elif (cls, "tutorial") not in schedule:
                session_type = "tutorial"
            else:
                continue

            for value in domains[cls][session_type]:
                day, time, room = value
                professor = course_instructor_mapping.get(cls)
                groups = course_group_mapping.get(cls, [])

                conflict = False
                for (c, typ), (p_day, p_time, p_room) in schedule.items():
                    if p_day == day and p_time == time:
                        if prof_schedule.get((c, typ)) == professor or p_room == room:
                            conflict = True
                            break

                for group in groups:
                    if (day, time) in student_group_schedule.get(group, set()):
                        conflict = True
                        break
                    next_slot = lecture_timeslots + tutorial_timeslots
                    if time in next_slot:
                        idx = next_slot.index(time)
                        previous_slot = next_slot[idx - 1] if idx > 0 else None
                        if previous_slot and (day, previous_slot) in student_group_schedule.get(group, set()):
                            conflict = True
                            break

                if conflict:
                    continue

                schedule[(cls, session_type)] = (day, time, room)
                prof_schedule[(cls, session_type)] = professor
                for group in groups:
                    student_group_schedule.setdefault(group, set()).add((day, time))

                result_schedule, result_profs = backtrack(schedule, prof_schedule, student_group_schedule)
                if result_schedule:
                    return result_schedule, result_profs

                del schedule[(cls, session_type)]
                del prof_schedule[(cls, session_type)]
                for group in groups:
                    student_group_schedule[group].remove((day, time))

        return None, None

    schedule = {}
    prof_schedule = {}
    student_group_schedule = {}
    solution, profs = backtrack(schedule, prof_schedule, student_group_schedule)

    if solution:
        db.session.query(ScheduledClass).delete()
        db.session.commit()
        for (cls, session_type), (day, time, room) in solution.items():
            scheduled_class = ScheduledClass(
                course=cls,
                instructor=course_instructor_mapping.get(cls),
                day=day,
                time=time,
                room=room,
                type=session_type
            )
            db.session.add(scheduled_class)
        db.session.commit()
        print("Timetable successfully scheduled!")
    else:
        print("No feasible timetable found.")
