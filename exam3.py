from datetime import datetime, timedelta
from models import Course, Students, Venue, Course_matrix
from sqlalchemy.sql import func
import json

def generate_exam_timetable():
    """
    Generate an exam timetable for courses, ensuring no exams during the break time (13:00–14:00).
    Courses are fetched in random order. Saves the timetable to a JSON file named exam_timetable_YYYY-MM-DD.json.

    Returns:
        List of dictionaries with exam schedules (day, date, time, venue, schedule)
        or None if no valid timetable can be generated.
    """
    # Fetch venue and student data from the database
    venue = {v.name: v.exam_capacity for v in Venue.query.all()}
    if not venue:
        print("No venues available.")
        return None

    student_groups = {s.programme: int(s.total_students) for s in Students.query.all()}
    if not student_groups:
        print("No student groups available.")
        return None

    # Fetch course-group mappings
    course_group_mapping = {}
    course_name_mapping = {}
    matrix_entries = Course_matrix.query.order_by(func.random()).all()
    for entry in matrix_entries:
        course = entry.course
        course_code = course.course_code
        course_name = course.course_name
        programme = entry.student.programme

        course_group_mapping.setdefault(course_code, [])
        if programme not in course_group_mapping[course_code]:
            course_group_mapping[course_code].append(programme)

        course_name_mapping[course_code] = course_name

    if not course_group_mapping:
        print("No course-group mappings available.")
        return None

    # Days and exam slots
    start_date = datetime.strptime("2023-04-30", "%Y-%m-%d")
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days = week_days * 4

    exam_timeslots = [
        "08:00-11:00",
        "11:30-14:30",
        "15:30-18:30"
    ]

    # Domain of valid timeslots for each course
    course_domains = {}
    for course_code, groups in course_group_mapping.items():
        try:
            total_students = sum(student_groups[group] for group in groups)
        except KeyError as e:
            print(f"Warning: Student group {e} not found for course {course_code}")
            continue

        valid_slots = [
            (day, timeslot, room)
            for day in days
            for timeslot in exam_timeslots
            for room, capacity in venue.items()
            if capacity >= total_students
        ]
        if valid_slots:
            course_domains[course_code] = valid_slots
        else:
            print(f"Warning: No valid slots for course {course_code}")

    all_courses = list(course_domains.keys())
    if not all_courses:
        print("No valid courses to schedule.")
        return None

    # Convert weekday and week index into date
    def get_actual_date(day_name, day_index):
        week_num = day_index // len(week_days)
        day_offset = day_index % len(week_days)
        week_start = start_date + timedelta(weeks=week_num)
        actual_date = week_start + timedelta(days=day_offset)
        return actual_date.strftime("%Y-%m-%d")

    # Backtracking search
    def backtrack(schedule, booked_timeslots, group_schedule):
        if len(schedule) == len(all_courses):
            return schedule

        unassigned_course = next(course for course in all_courses if course not in schedule)

        for day, timeslot, room in course_domains[unassigned_course]:
            groups = course_group_mapping.get(unassigned_course, [])
            conflict = False

            if (day, timeslot, room) in booked_timeslots:
                continue

            try:
                total_students = sum(student_groups[group] for group in groups)
                if venue[room] < total_students:
                    continue
            except KeyError:
                continue

            for group in groups:
                if (day, timeslot) in group_schedule.get(group, set()):
                    conflict = True
                    break

            if conflict:
                continue

            # Assign
            schedule[unassigned_course] = (day, timeslot, room, groups)
            booked_timeslots.add((day, timeslot, room))
            for group in groups:
                group_schedule.setdefault(group, set()).add((day, timeslot))

            result = backtrack(schedule, booked_timeslots, group_schedule)
            if result:
                return result

            # Undo
            del schedule[unassigned_course]
            booked_timeslots.remove((day, timeslot, room))
            for group in groups:
                group_schedule[group].remove((day, timeslot))

        return None

    # Start search
    final_schedule = backtrack({}, set(), {})

    if not final_schedule:
        print("No valid exam timetable could be generated.")
        return None

    # Construct output with formatted group names and student counts
    final_schedule_with_dates = []
    for course, (day, timeslot, room, groups) in final_schedule.items():
        day_index = days.index(day)
        actual_date = get_actual_date(day, day_index)

        formatted_groups = []
        total_students = 0
        for group in groups:
            count = student_groups.get(group, 0)
            total_students += count
            formatted_groups.append(f"{group} ({count})")

        # Format the timetable entry like the image
        course_info = f"{course} {course_name_mapping.get(course, 'Unknown Course')}"
        groups_str = ", ".join(formatted_groups)
        timetable_entry = f"{course_info}: {groups_str} [Total: {total_students}]"

        final_schedule_with_dates.append({
            "day": day,
            "date": actual_date,
            "time": timeslot,
            "venue": room,  # Use the assigned room from backtracking
            "schedule": timetable_entry
        })

    # Sort by date and time
    time_order = {slot: idx for idx, slot in enumerate(exam_timeslots)}
    final_schedule_with_dates.sort(key=lambda x: (
        datetime.strptime(x["date"], "%Y-%m-%d"),
        time_order[x["time"]]
    ))

    # Save to file
    current_date = datetime.now().strftime("%Y-%m-%d")
    json_filename = f"exam_timetable_{current_date}.json"
    try:
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(final_schedule_with_dates, f, indent=4, ensure_ascii=False)
        print(f"Exam timetable saved to {json_filename}")
    except IOError as e:
        print(f"Warning: Failed to save JSON file {json_filename}: {e}")

    return final_schedule_with_dates

