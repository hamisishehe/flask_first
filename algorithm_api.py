from flask import json, jsonify, request
from fpdf import FPDF
from datetime import datetime, timedelta
from models import db, Course, Students, Venue, Instructor, Course_matrix
from sqlalchemy.sql import func

def generate_timetable(app, semester, s_start_time):
    """
    Generate a timetable scheduling lectures, tutorials, and practicals for courses in the specified semester.
    Courses are fetched in random order. Ensures no sessions are scheduled during the break time (13:00–14:00) 
    and no conflicts in instructor, room, or student group assignments, with rest gaps for lectures. Saves the 
    timetable to a JSON file named timetable_semester_{semester}.json.
    
    gg
    Args:
        app: Flask application instance for database context.
        semester: Integer (1 or 2) to filter courses by semester.
        s_start_time: String representing the start time for lecture slots (e.g., "07:30").
    
    Returns:
        List of dictionaries with course schedules (course_code, course_name, session_type, day, time, venue, 
        instructor, groups, semester) or error message.
    """
    with app.app_context():
        # Print all unique program_group values
        program_groups = list(set(entry.program_group for entry in Course_matrix.query.all() if entry.program_group is not None))
        print("Program Groups:", program_groups)

        # Validate semester input
        if semester not in [1, 2]:
            return {"error": "Invalid semester: must be 1 or 2"}

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
        course_name_mapping = {}
        # Fetch courses in random order for the specified semester
        for entry in Course_matrix.query.join(Course).filter(Course.semester == semester).order_by(func.random()).all():
            course = entry.course
            course_code = course.course_code
            course_name = course.course_name
            programme = entry.student.programme
            instructor = entry.instructor

            # Validate that at least one session type is enabled
            if not (course.is_lecture or course.is_tutorial or course.is_practical):
                print(f"Warning: Course {course_code} has no session types (lecture, tutorial, practical)")
                continue

            # Course-group mapping
            course_group_mapping.setdefault(course_code, [])
            if programme not in course_group_mapping[course_code]:
                course_group_mapping[course_code].append(programme)

            # Instructor mapping
            full_name = f"{instructor.first_name} {instructor.middle_name + ' ' if instructor.middle_name else ''}{instructor.last_name or ''}".strip()
            title = instructor.title or "Mr./Ms."
            course_instructor_mapping[course_code] = f"{title}. {full_name}"

            # Session types
            course_session_types[course_code] = {
                "is_lecture": course.is_lecture,
                "is_tutorial": course.is_tutorial,
                "is_practical": course.is_practical
            }

            # Course name mapping
            course_name_mapping[course_code] = course_name

        if not course_group_mapping:
            return {"error": f"No course-group mappings available for semester {semester}"}

        # Step 3: Define time slots
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        # Lecture slots: 07:30–13:00, 2-hour blocks, excluding 13:00–14:00 break
        start_time = datetime.strptime(s_start_time, "%H:%M")
        timeslots = [
            (start_time + timedelta(hours=2 * i)).strftime("%H:%M") + "-" +
            (start_time + timedelta(hours=2 * (i + 1))).strftime("%H:%M") for i in range(2)  # 07:30–09:30, 09:30–11:30
        ]
        # Add 11:30–13:00 slot (1.5 hours to respect break time)
        timeslots.append("11:30-13:00")

        # Tutorial slots: 17:30–19:30, 1-hour blocks (unaffected by break time)
        tutorial_start = datetime.strptime("17:30", "%H:%M")
        tutorial_slots = [(tutorial_start + timedelta(hours=i)).strftime("%H:%M") + "-" +
                          (tutorial_start + timedelta(hours=i + 1)).strftime("%H:%M") for i in range(2)]

        # Practical slots: 15:30–19:30, 2-hour blocks (unaffected by break time)
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
                else:
                    print(f"Warning: No valid lecture slots for course {cls}")

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
                else:
                    print(f"Warning: No valid tutorial slots for course {cls}")

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
                else:
                    print(f"Warning: No valid practical slots for course {cls}")

        # Step 5: Combine all courses to schedule
        all_courses = list(lecture_domains.keys()) + list(tutorial_domains.keys()) + list(practical_domains.keys())
        if not all_courses:
            return {"error": f"No valid courses to schedule for semester {semester}"}

        # Optimize: Sort courses by domain size (fewest slots first) for faster backtracking
        all_courses.sort(key=lambda cls: len(lecture_domains.get(cls, []) + 
                                           tutorial_domains.get(cls, []) + 
                                           practical_domains.get(cls, [])))

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
                # Extract base course code: remove suffixes for tutorials/practicals; lectures use raw code
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

                    # Rest gap for lectures only (check adjacent slots)
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
                # Extract base course code: remove suffixes for tutorials/practicals; lectures use raw code
                course_code = cls.replace(" (Tutorial)", "").replace(" (Practical)", "")
                session_type = "Tutorial" if "Tutorial" in cls else "Practical" if "Practical" in cls else "Lecture"
                instructor = instructor_assignments.get(cls, "Unknown Instructor")
                groups = course_group_mapping.get(course_code, [])
                course_name = course_name_mapping.get(course_code, "Unknown Course")

                timetable.append({
                    "course_code": course_code,
                    "course_name": course_name,
                    "session_type": session_type,
                    "day": day,
                    "time": time,
                    "venue": room,
                    "instructor": instructor,
                    "groups": groups,
                    "semester": semester
                })

            # Sort by day and time for consistent output
            day_order = {day: index for index, day in enumerate(days)}
            time_order = {time: index for index, time in enumerate(timeslots + tutorial_slots + practical_slots)}
            timetable.sort(key=lambda x: (day_order[x['day']], time_order[x['time']]))

            # Save timetable to JSON file
            json_filename = f"timetable_semester_{semester}.json"
            try:
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(timetable, f, indent=4, ensure_ascii=False)
            except IOError as e:
                print(f"Warning: Failed to save JSON file {json_filename}: {e}")

            return timetable
        else:
            return {"error": f"No valid timetable could be generated for semester {semester}"}