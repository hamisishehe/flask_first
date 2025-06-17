from flask import json
from fpdf import FPDF
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, Course, Students, Venue, Instructor, Course_matrix

def parse_time_range(time_range):
    start_str, end_str = time_range.split("-")
    start_time = datetime.strptime(start_str.strip(), "%H:%M")
    end_time = datetime.strptime(end_str.strip(), "%H:%M")
    return start_time, end_time

def times_overlap(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

def generate_timetable(app, semester, t_start_time, b_start_time, b_end_time, t_days):
    with app.app_context():
        venues = {v.name: v.teaching_capacity for v in Venue.query.all()}
        if not venues:
            return {"error": "No venues available"}

        student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}
        if not student_groups:
            return {"error": "No student groups available"}

        course_group_mapping = {}
        course_program_groups_mapping = {}
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
            program_group = entry.program_group

            if course_code not in course_group_mapping:
                course_group_mapping[course_code] = set()
            if course_code not in course_program_groups_mapping:
                course_program_groups_mapping[course_code] = set()

            course_group_mapping[course_code].add(programme)
            if program_group:
                course_program_groups_mapping[course_code].add(program_group)

            instructor_name = f"{instructor.title or 'Mr./Ms.'} {instructor.first_name} {instructor.middle_name or ''} {instructor.last_name or ''}".strip()
            course_instructor_mapping[course_code] = instructor_name
            course_session_types[course_code] = {
                "is_lecture": course.is_lecture,
                "is_tutorial": course.is_tutorial,
                "is_practical": course.is_practical,
            }
            course_name_mapping[course_code] = course_name

        for k in course_group_mapping:
            course_group_mapping[k] = list(course_group_mapping[k])
        for k in course_program_groups_mapping:
            course_program_groups_mapping[k] = list(course_program_groups_mapping[k])

        days = t_days
        start_time = datetime.strptime(t_start_time, "%H:%M")
        lunch_start = datetime.strptime(b_start_time, "%H:%M")
        lunch_end = datetime.strptime(b_end_time, "%H:%M")

        def slot_overlaps_lunch(slot_start, slot_end):
            return times_overlap(slot_start, slot_end, lunch_start, lunch_end)

        raw_lecture_slots = [(start_time + timedelta(hours=2*i), start_time + timedelta(hours=2*(i+1))) for i in range(5)]
        lecture_slots = [ (s,e) for (s,e) in raw_lecture_slots if not slot_overlaps_lunch(s, e) ]

        raw_tutorial_slots = [(start_time + timedelta(hours=i), start_time + timedelta(hours=i+1)) for i in range(9)]
        tutorial_slots = [ (s,e) for (s,e) in raw_tutorial_slots if not slot_overlaps_lunch(s, e) ]

        practical_slots = lecture_slots

        lecture_domains, tutorial_domains, practical_domains = {}, {}, {}

        for course_code, groups in course_group_mapping.items():
            try:
                total_students = sum(student_groups[group] for group in groups)
            except KeyError:
                continue

            suitable_venues = [room for room, capacity in venues.items() if capacity >= total_students]
            if not suitable_venues:
                continue

            if course_session_types[course_code]["is_lecture"]:
                lecture_domains[course_code] = [(day, f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}", room)
                                                for day in days for s,e in lecture_slots for room in suitable_venues]
            if course_session_types[course_code]["is_tutorial"]:
                tutorial_domains[course_code] = [(day, f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}", room)
                                                 for day in days for s,e in tutorial_slots for room in suitable_venues]
            if course_session_types[course_code]["is_practical"]:
                practical_domains[course_code] = [(day, f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}", room)
                                                  for day in days for s,e in practical_slots for room in suitable_venues]

        all_sessions = []
        for course_code in course_group_mapping.keys():
            if course_session_types[course_code]["is_lecture"]:
                all_sessions.append((course_code, "Lecture"))
            if course_session_types[course_code]["is_tutorial"]:
                all_sessions.append((course_code, "Tutorial"))
            if course_session_types[course_code]["is_practical"]:
                all_sessions.append((course_code, "Practical"))

        def backtrack(assignments, instructor_schedule, student_schedule, venue_schedule, index=0):
            if index == len(all_sessions):
                return assignments

            course_code, session_type = all_sessions[index]
            domain = (lecture_domains if session_type == "Lecture" else
                      tutorial_domains if session_type == "Tutorial" else
                      practical_domains).get(course_code, [])

            duration = 2 if session_type in ["Lecture", "Practical"] else 1
            instructor = course_instructor_mapping[course_code]
            groups = course_group_mapping[course_code]

            for (day, time_range, room) in domain:
                start_time_slot, end_time_slot = parse_time_range(time_range)

                if any(times_overlap(start_time_slot, end_time_slot, s, e) for d, s, e in venue_schedule.get(room, []) if d == day):
                    continue
                if any(times_overlap(start_time_slot, end_time_slot, s, e) for d, s, e in instructor_schedule.get(instructor, []) if d == day):
                    continue
                if any(times_overlap(start_time_slot, end_time_slot, s, e) for group in groups for d, s, e in student_schedule.get(group, []) if d == day):
                    continue

                assignments[(course_code, session_type)] = (day, time_range, room)
                venue_schedule.setdefault(room, []).append((day, start_time_slot, end_time_slot))
                instructor_schedule.setdefault(instructor, []).append((day, start_time_slot, end_time_slot))
                for group in groups:
                    student_schedule.setdefault(group, []).append((day, start_time_slot, end_time_slot))

                result = backtrack(assignments, instructor_schedule, student_schedule, venue_schedule, index + 1)
                if result:
                    return result

                del assignments[(course_code, session_type)]
                venue_schedule[room].remove((day, start_time_slot, end_time_slot))
                instructor_schedule[instructor].remove((day, start_time_slot, end_time_slot))
                for group in groups:
                    student_schedule[group].remove((day, start_time_slot, end_time_slot))

            return None

        assignments = {}
        result = backtrack(assignments, {}, {}, {})
        if not result:
            return {"error": "No valid timetable could be generated without conflicts."}

        day_order = {day: i for i, day in enumerate(days)}
        def get_start_time(t): return datetime.strptime(t.split("-")[0], "%H:%M")

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
                "groups": course_group_mapping.get(course_code, [])  +  course_program_groups_mapping.get(course_code, [] ),
            })

        timetable.sort(key=lambda x: (day_order[x["day"]], get_start_time(x["time"])))
        return timetable
