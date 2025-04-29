from flask import json
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix

def generate_timetable(app):
    with app.app_context(): 

        ## Step 1: Problem variables
        
        venue = {v.name: v.teaching_capacity for v in Venue.query.all()}
        student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}

        course_group_mapping = {}
        matrix_entries = Course_matrix.query.all()
        for entry in matrix_entries:
            course_code = entry.course.course_code  # changed here
            programme = entry.student.programme
            course_group_mapping.setdefault(course_code, [])
            if programme not in course_group_mapping[course_code]:
                course_group_mapping[course_code].append(programme)

        course_instructor_mapping = {}
        for entry in matrix_entries:
            course_code = entry.course.course_code  # changed here
            instructor = entry.instructor
            full_name = f"{instructor.first_name} {instructor.middle_name + ' ' if instructor.middle_name else ''}{instructor.last_name or ''}".strip()
            title = instructor.title or "Mr./Ms."
            instructor_display = f"{title}. {full_name}"
            course_instructor_mapping[course_code] = instructor_display

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        start_time = datetime.strptime("07:30", "%H:%M")
        timeslots = [(start_time + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
             (start_time + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(4)]


        # Include tutorial timeslots (1 hour slots in afternoon)
        tutorial_start = datetime.strptime("17:30", "%H:%M")
        tutorial_slots = [(tutorial_start + timedelta(hours=i)).strftime("%H:%M") + "-" +
                          (tutorial_start + timedelta(hours=i + 1)).strftime("%H:%M") for i in range(2)]

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

        def backtrack(schedule, instructor_schedule, student_group_schedule):
            if len(schedule) == len(all_courses):
                return schedule, instructor_schedule

            unassigned_class = next(cls for cls in all_courses if cls not in schedule)

            domains = lecture_domains if "Tutorial" not in unassigned_class else tutorial_domains
            for value in domains[unassigned_class]:
                day, time, room = value
                course_code = unassigned_class.replace(" (Tutorial)", "")  # changed here
                instructor = course_instructor_mapping.get(course_code)
                groups = course_group_mapping.get(course_code, [])

                conflict = False
                for existing_cls, (p_day, p_time, p_room) in schedule.items():
                    if p_day == day and p_time == time:
                        if instructor_schedule.get(existing_cls) == instructor or p_room == room:
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
                instructor_schedule[unassigned_class] = instructor
                for group in groups:
                    student_group_schedule.setdefault(group, set()).add((day, time))

                result_schedule, result_profs = backtrack(schedule, instructor_schedule, student_group_schedule)
                if result_schedule:
                    return result_schedule, result_profs

                del schedule[unassigned_class]
                del instructor_schedule[unassigned_class]
                for group in groups:
                    student_group_schedule[group].remove((day, time))

            return None, None

        schedule = {}
        instructor_schedule = {}
        student_group_schedule = {}
        solution, instructor_assignments = backtrack(schedule, instructor_schedule, student_group_schedule)

        if solution:
            timetable = []
            for cls, (day, time, room) in solution.items():
                course_code = cls.replace(" (Tutorial)", "")  # changed here
                session_type = "Tutorial" if "Tutorial" in cls else "Lecture"
                instructor = instructor_assignments.get(cls, "Unknown Instructor")
                groups = course_group_mapping.get(course_code, [])

                timetable.append({
                    "course_code": course_code,
                    "session_type": session_type,
                    "day": day,
                    "time": time,
                    "venue": room,
                    "instructor": instructor,
                    "groups":groups
                })

                day_order = {day: index for index, day in enumerate(days)}
                time_order = {time: index for index, time in enumerate(timeslots + tutorial_slots)}

                timetable.sort(key=lambda x: (day_order[x['day']], time_order[x['time']]))

            return timetable
        
        else:
            return None
