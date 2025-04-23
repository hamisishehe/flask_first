from flask import json
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix

def generate_timetable(app):
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
            timetable = []
            for cls, (day, time, room) in solution.items():
                course_name = cls.replace(" (Tutorial)", "")
                is_tutorial = "Tutorial" in cls
                instructor = instructor_assignments.get(course_name, "Unknown")
                groups = course_group_mapping.get(course_name, [])

                timetable.append({
                    "day": day,
                    "time": time,
                    "Course": cls,
                    "is_tutorial": is_tutorial,
                    "Venue": room,
                    "instructor": instructor,
                    "groups": groups
                })


                with open('last_timetable.json', 'w') as json_file:
                    json.dump(timetable, json_file)

            return timetable
        else:
            raise Exception("No valid timetable could be generated.")

