from flask import json
from fpdf import FPDF
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, Course, Students, Venue, Instructor, Course_matrix
from datetime import datetime, timedelta

def parse_time_range(time_range):
    start_str, end_str = time_range.split("-")
    start_time = datetime.strptime(start_str.strip(), "%H:%M")
    end_time = datetime.strptime(end_str.strip(), "%H:%M")
    return start_time, end_time

def times_overlap(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

def generate_timetable(app, semester, t_start_time):
    with app.app_context():
        # Fetch venues and capacities
        venues = {v.name: v.teaching_capacity for v in Venue.query.all()}
        if not venues:
            return {"error": "No venues available"}

        # Fetch student group sizes
        student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}
        if not student_groups:
            return {"error": "No student groups available"}

        # Fetch courses for semester and build maps
        course_group_mapping = {}
        course_instructor_mapping = {}
        course_session_types = {}
        course_name_mapping = {}

        course_matrix_entries = Course_matrix.query.join(Course).filter(Course.semester == semester).all()
        if not course_matrix_entries:
            return {"error": "No courses found for the semester"}

        for entry in course_matrix_entries:
            course = entry.course
            course_code = course.course_code
            course_name = course.course_name
            programme = entry.student.programme
            instructor = entry.instructor
            if course_code not in course_group_mapping:
                course_group_mapping[course_code] = set()
            course_group_mapping[course_code].add(programme)

            instructor_name = f"{instructor.title or 'Mr./Ms.'} {instructor.first_name} {instructor.middle_name or ''} {instructor.last_name or ''}".strip()
            course_instructor_mapping[course_code] = instructor_name
            course_session_types[course_code] = {
                "is_lecture": course.is_lecture,
                "is_tutorial": course.is_tutorial,
                "is_practical": course.is_practical,
            }
            course_name_mapping[course_code] = course_name

        # Convert groups from set to list for iteration
        for k in course_group_mapping:
            course_group_mapping[k] = list(course_group_mapping[k])

        # Days and starting time
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        start_time = datetime.strptime(t_start_time, "%H:%M")

        # Define time slots
        # Lecture: 2 hours slots, e.g. 7:30-9:30, 9:30-11:30, ...
        lecture_slots = [(start_time + timedelta(hours=2*i),
                          start_time + timedelta(hours=2*(i+1))) for i in range(4)]
        # Tutorial: 1 hour slots within the same period
        tutorial_slots = [(start_time + timedelta(hours=i),
                           start_time + timedelta(hours=i+1)) for i in range(8)]  # More 1-hr slots
        # Practical: 2 hours slots but fewer, can overlap with tutorials differently
        practical_slots = lecture_slots  # same as lecture for duration 2h

        # Build domains for each session type
        lecture_domains = {}
        tutorial_domains = {}
        practical_domains = {}

        for course_code, groups in course_group_mapping.items():
            try:
                total_students = sum(student_groups[group] for group in groups)
            except KeyError:
                continue

            # Find venues with enough capacity
            suitable_venues = [room for room, capacity in venues.items() if capacity >= total_students]
            if not suitable_venues:
                continue

            if course_session_types[course_code]["is_lecture"]:
                lecture_domains[course_code] = []
                for day in days:
                    for slot_start, slot_end in lecture_slots:
                        time_range = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
                        for room in suitable_venues:
                            lecture_domains[course_code].append((day, time_range, room))

            if course_session_types[course_code]["is_tutorial"]:
                tutorial_domains[course_code] = []
                for day in days:
                    for slot_start, slot_end in tutorial_slots:
                        time_range = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
                        for room in suitable_venues:
                            tutorial_domains[course_code].append((day, time_range, room))

            if course_session_types[course_code]["is_practical"]:
                practical_domains[course_code] = []
                for day in days:
                    for slot_start, slot_end in practical_slots:
                        time_range = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
                        for room in suitable_venues:
                            practical_domains[course_code].append((day, time_range, room))

        all_sessions = []
        # For each course, create a session per type that applies, with label to differentiate in assignment
        for course_code in course_group_mapping.keys():
            if course_session_types[course_code]["is_lecture"]:
                all_sessions.append((course_code, "Lecture"))
            if course_session_types[course_code]["is_tutorial"]:
                all_sessions.append((course_code, "Tutorial"))
            if course_session_types[course_code]["is_practical"]:
                all_sessions.append((course_code, "Practical"))

        # Backtracking scheduler
        def backtrack(assignments, instructor_schedule, student_schedule, venue_schedule, index=0):
            if index == len(all_sessions):
                return assignments

            course_code, session_type = all_sessions[index]
            if session_type == "Lecture":
                domain = lecture_domains.get(course_code, [])
                duration = 2
            elif session_type == "Tutorial":
                domain = tutorial_domains.get(course_code, [])
                duration = 1
            else:  # Practical
                domain = practical_domains.get(course_code, [])
                duration = 2

            instructor = course_instructor_mapping[course_code]
            groups = course_group_mapping[course_code]

            for (day, time_range, room) in domain:
                start_time, end_time = parse_time_range(time_range)

                conflict = False

                # Check venue conflicts
                if room in venue_schedule:
                    for (v_day, v_start, v_end) in venue_schedule[room]:
                        if v_day == day and times_overlap(v_start, v_end, start_time, end_time):
                            conflict = True
                            break
                if conflict:
                    continue

                # Check instructor conflicts
                if instructor in instructor_schedule:
                    for (i_day, i_start, i_end) in instructor_schedule[instructor]:
                        if i_day == day and times_overlap(i_start, i_end, start_time, end_time):
                            conflict = True
                            break
                if conflict:
                    continue

                # Check student groups conflicts
                for group in groups:
                    if group in student_schedule:
                        for (g_day, g_start, g_end) in student_schedule[group]:
                            if g_day == day and times_overlap(g_start, g_end, start_time, end_time):
                                conflict = True
                                break
                    if conflict:
                        break
                if conflict:
                    continue

                # No conflicts, assign this slot
                assignments[(course_code, session_type)] = (day, time_range, room)

                # Update schedules
                venue_schedule.setdefault(room, []).append((day, start_time, end_time))
                instructor_schedule.setdefault(instructor, []).append((day, start_time, end_time))
                for group in groups:
                    student_schedule.setdefault(group, []).append((day, start_time, end_time))

                result = backtrack(assignments, instructor_schedule, student_schedule, venue_schedule, index + 1)
                if result:
                    return result

                # Backtrack - remove from schedules
                del assignments[(course_code, session_type)]
                venue_schedule[room].remove((day, start_time, end_time))
                instructor_schedule[instructor].remove((day, start_time, end_time))
                for group in groups:
                    student_schedule[group].remove((day, start_time, end_time))

            return None

        assignments = {}
        result = backtrack(assignments, {}, {}, {})

        if not result:
            return {"error": "No valid timetable could be generated without conflicts."}

        # Format the timetable output
        timetable = []
        for (course_code, session_type), (day, time_range, room) in result.items():
            timetable.append({
                "course_code": course_code,
                "course_name": course_name_mapping.get(course_code, "Unknown Course"),
                "session_type": session_type,
                "day": day,
                "time": time_range,
                "venue": room,
                "instructor": course_instructor_mapping.get(course_code, "Unknown Instructor"),
                "groups": course_group_mapping.get(course_code, [])
            })

        # Sort timetable by day and start time
        day_order = {day: i for i, day in enumerate(days)}
        def get_start_time(t):
            return datetime.strptime(t.split("-")[0], "%H:%M")
        timetable.sort(key=lambda x: (day_order[x["day"]], get_start_time(x["time"])))

        return timetable
