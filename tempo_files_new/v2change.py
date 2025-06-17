from flask import json
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix


def generate_timetable(app):
    with app.app_context():
        # Step 1: Initialize problem variables
        venues = {v.name: v.teaching_capacity for v in Venue.query.all()}
        if not venues:
            return {"error": "No venues available"}

        student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}
        if not student_groups:
            return {"error": "No student groups available"}

        # Step 2: Build mappings for courses, groups, instructors, and session types
        course_group_mapping = {}
        course_instructor_mapping = {}
        course_session_types = {}
        for entry in Course_matrix.query.all():
            course = entry.course
            course_code = course.course_code
            programme = entry.student.programme
            instructor = entry.instructor

            # Course-group mapping
            course_group_mapping.setdefault(course_code, [])
            if programme not in course_group_mapping[course_code]:
                course_group_mapping[course_code].append(programme)

            # Instructor mapping
            full_name = f"{instructor.first_name} {instructor.middle_name + ' ' if instructor.middle_name else ''}{instructor.last_name or ''}".strip()
            title = instructor.title or "Mr./Ms."
            course_instructor_mapping[course_code] = f"{title}. {full_name}"

            # Session types (lecture, tutorial, practical)
            course_session_types[course_code] = {
                "is_lecture": course.is_lecture,
                "is_tutorial": course.is_tutorial,
                "is_practical": course.is_practical
            }

        if not course_group_mapping:
            return {"error": "No course-group mappings available"}

        # Step 3: Define time slots
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        # Lecture slots: 07:30-15:30, 2-hour blocks
        start_time = datetime.strptime("07:30", "%H:%M")
        timeslots = [(start_time + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
                     (start_time + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(4)]

        # Tutorial slots: 17:30-19:30, 1-hour blocks
        tutorial_start = datetime.strptime("17:30", "%H:%M")
        tutorial_slots = [(tutorial_start + timedelta(hours=i)).strftime("%H:%M") + "-" +
                          (tutorial_start + timedelta(hours=i + 1)).strftime("%H:%M") for i in range(2)]

        # Practical slots: 15:30-19:30, 2-hour blocks
        practical_start = datetime.strptime("15:30", "%H:%M")
        practical_slots = [(practical_start + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
                           (practical_start + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(2)]

        # Step 4: Create domains for each session type
        lecture_domains = {}
        tutorial_domains = {}
        practical_domains = {}
        for cls, groups in course_group_mapping.items():
            try:
                total_students = sum(student_groups[group] for group in groups)
            except KeyError as e:
                print(f"Warning: Student group {e} not found for course {cls}")
                continue

            # Lecture domains
            if course_session_types[cls]["is_lecture"]:
                valid_lecture_slots = [
                    (day, slot, room)
                    for day in days
                    for slot in timeslots
                    for room in venues
                    if venues[room] >= total_students
                ]
                if valid_lecture_slots:
                    lecture_domains[cls] = valid_lecture_slots

            # Tutorial domains
            if course_session_types[cls]["is_tutorial"]:
                valid_tutorial_slots = [
                    (day, slot, room)
                    for day in days
                    for slot in tutorial_slots
                    for room in venues
                    if venues[room] >= total_students
                ]
                if valid_tutorial_slots:
                    tutorial_domains[cls + " (Tutorial)"] = valid_tutorial_slots

            # Practical domains
            if course_session_types[cls]["is_practical"]:
                valid_practical_slots = [
                    (day, slot, room)
                    for day in days
                    for slot in practical_slots
                    for room in venues
                    if venues[room] >= total_students
                ]
                if valid_practical_slots:
                    practical_domains[cls + " (Practical)"] = valid_practical_slots

        # Step 5: Combine all courses to schedule
        all_courses = list(lecture_domains.keys()) + list(tutorial_domains.keys()) + list(practical_domains.keys())
        if not all_courses:
            return {"error": "No valid courses to schedule"}

        # Step 6: Backtracking algorithm to schedule courses
        def backtrack(schedule, instructor_schedule, student_group_schedule):
            if len(schedule) == len(all_courses):
                return schedule, instructor_schedule

            unassigned_class = next(cls for cls in all_courses if cls not in schedule)
            if "Tutorial" in unassigned_class:
                domains = tutorial_domains
            elif "Practical" in unassigned_class:
                domains = practical_domains
            else:
                domains = lecture_domains

            for value in domains[unassigned_class]:
                day, time, room = value
                course_code = unassigned_class.replace(" (Tutorial)", "").replace(" (Practical)", "")
                instructor = course_instructor_mapping.get(course_code)
                groups = course_group_mapping.get(course_code, [])

                # Check for conflicts
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

                    # Rest gap for lectures only
                    if "Tutorial" not in unassigned_class and "Practical" not in unassigned_class:
                        idx = timeslots.index(time) if time in timeslots else -1
                        if idx > 0 and (day, timeslots[idx - 1]) in student_group_schedule.get(group, set()):
                            conflict = True
                            break
                        if idx < len(timeslots) - 1 and (day, timeslots[idx + 1]) in student_group_schedule.get(group, set()):
                            conflict = True
                            break

                if conflict:
                    continue

                # Assign the slot
                schedule[unassigned_class] = (day, time, room)
                instructor_schedule[unassigned_class] = instructor
                for group in groups:
                    student_group_schedule.setdefault(group, set()).add((day, time))

                # Recurse
                result_schedule, result_profs = backtrack(schedule, instructor_schedule, student_group_schedule)
                if result_schedule:
                    return result_schedule, result_profs

                # Backtrack: undo assignment
                del schedule[unassigned_class]
                del instructor_schedule[unassigned_class]
                for group in groups:
                    student_group_schedule[group].remove((day, time))

            return None, None

        # Step 7: Run backtracking
        schedule = {}
        instructor_schedule = {}
        student_group_schedule = {}
        solution, instructor_assignments = backtrack(schedule, instructor_schedule, student_group_schedule)

        # Step 8: Format and return timetable
        if solution:
            timetable = []
            for cls, (day, time, room) in solution.items():
                course_code = cls.replace(" (Tutorial)", "").replace(" (Practical)", "")
                session_type = "Tutorial" if "Tutorial" in cls else "Practical" if "Practical" in cls else "Lecture"
                instructor = instructor_assignments.get(cls, "Unknown Instructor")
                groups = course_group_mapping.get(course_code, [])

                timetable.append({
                    "course_code": course_code,
                    "session_type": session_type,
                    "day": day,
                    "time": time,
                    "venue": room,
                    "instructor": instructor,
                    "groups": groups
                })

            # Sort by day and time
            day_order = {day: index for index, day in enumerate(days)}
            time_order = {time: index for index, time in enumerate(timeslots + tutorial_slots + practical_slots)}
            timetable.sort(key=lambda x: (day_order[x['day']], time_order[x['time']]))

            return timetable
        else:
            return {"error": "No valid timetable could be generated"}