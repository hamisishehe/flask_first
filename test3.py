from fpdf import FPDF, XPos, YPos
from datetime import datetime, timedelta
import random

# Step 1: Problem variables

classes = [
    'Math', 'Physics', 'Chemistry', 'Biology', 'ComputerScience',
    'English', 'History', 'Geography', 'Art', 'Economics',
    'Philosophy', 'Statistics', 'Business', 'Accounting', 'Drama',
    'Sociology', 'Law', 'PoliticalScience', 'EnvironmentalScience', 'Psychology'
]

professors = [f"Prof_{chr(65+i)}" for i in range(20)]

# Rooms and their capacities
rooms = {
    'Room_1': 50,
    'Room_2': 60,
    'Room_3': 80,
    'Room_4': 100,
    'Room_5': 120,
    'Room_6': 90,
    'Room_7': 70,
    'Room_8': 110,
    'Room_9': 60,
    'Room_10': 100
}

# Days and timeslots (2-hour intervals)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
start_time = datetime.strptime("08:00", "%H:%M")
timeslots = [(start_time + timedelta(hours=2*i)).strftime("%H:%M") + "-" +
             (start_time + timedelta(hours=2*(i+1))).strftime("%H:%M") for i in range(5)]

# Student groups and sizes
student_groups = {
    'ComputerEngineering': 80,
    'ElectricalEngineering': 60,
    'BusinessStudies': 100,
    'Law': 50
}

# Assign each subject to multiple groups (same class can have more than one group)
class_group_mapping = {
    'Math': ['ComputerEngineering', 'ElectricalEngineering'],
    'Physics': ['ComputerEngineering', 'ElectricalEngineering'],
    'Chemistry': ['ComputerEngineering'],
    'Biology': ['ElectricalEngineering'],
    'ComputerScience': ['ComputerEngineering'],
    'English': ['BusinessStudies'],
    'History': ['Law'],
    'Geography': ['BusinessStudies'],
    'Art': ['BusinessStudies'],
    'Economics': ['BusinessStudies'],
    'Philosophy': ['Law'],
    'Statistics': ['ComputerEngineering'],
    'Business': ['BusinessStudies'],
    'Accounting': ['BusinessStudies'],
    'Drama': ['BusinessStudies'],
    'Sociology': ['Law'],
    'Law': ['Law'],
    'PoliticalScience': ['Law'],
    'EnvironmentalScience': ['ElectricalEngineering'],
    'Psychology': ['Law']
}

# Assign professors to each class
class_professor_mapping = {
    'Math': 'Prof_A',
    'Physics': 'Prof_B',
    'Chemistry': 'Prof_C',
    'Biology': 'Prof_D',
    'ComputerScience': 'Prof_E',
    'English': 'Prof_F',
    'History': 'Prof_G',
    'Geography': 'Prof_H',
    'Art': 'Prof_I',
    'Economics': 'Prof_J',
    'Philosophy': 'Prof_K',
    'Statistics': 'Prof_L',
    'Business': 'Prof_M',
    'Accounting': 'Prof_N',
    'Drama': 'Prof_O',
    'Sociology': 'Prof_P',
    'Law': 'Prof_Q',
    'PoliticalScience': 'Prof_R',
    'EnvironmentalScience': 'Prof_S',
    'Psychology': 'Prof_T'
}

# Step 2: Generate domains with room capacity constraint
domains = {
    cls: [
        (day, slot, room) for day in days for slot in timeslots
        for room in rooms if rooms[room] >= max(student_groups[group] for group in class_group_mapping[cls])
    ]
    for cls in classes
}

# Step 3: Constraints
def no_conflict(schedule):
    scheduled = [(val[0], val[1]) for val in schedule.values()]
    return len(scheduled) == len(set(scheduled))

def room_availability(schedule):
    day_time_room = [(val[0], val[1], val[2]) for val in schedule.values()]
    return len(day_time_room) == len(set(day_time_room))

def professor_availability(schedule, prof_schedule):
    prof_times = [(prof, val[0], val[1]) for prof, val in prof_schedule.items()]
    return len(prof_times) == len(set(prof_times))

# Step 4: Backtracking Search
def backtrack(schedule, domains, prof_schedule):
    if len(schedule) == len(classes):
        if no_conflict(schedule) and room_availability(schedule) and professor_availability(schedule, prof_schedule):
            return schedule, prof_schedule
        return None, None

    unassigned_class = next(cls for cls in classes if cls not in schedule)
    random.shuffle(professors)  # Try professors in random order

    for value in domains[unassigned_class]:  # (day, time, room)
        day, time, room = value
        professor = class_professor_mapping[unassigned_class]  # Get the assigned professor
        if all(not (p_day == day and p_time == time) for p_cls, (p_day, p_time, _) in schedule.items() if prof_schedule.get(p_cls) == professor):
            schedule[unassigned_class] = (day, time, room)
            prof_schedule[unassigned_class] = professor
            if no_conflict(schedule) and room_availability(schedule) and professor_availability(schedule, prof_schedule):
                result_schedule, result_profs = backtrack(schedule, domains, prof_schedule)
                if result_schedule:
                    return result_schedule, result_profs
            del schedule[unassigned_class]
            del prof_schedule[unassigned_class]
    return None, None

# Step 5: Solve
schedule = {}
prof_schedule = {}
solution, instructor_assignments = backtrack(schedule, domains, prof_schedule)

# Step 6: Generate PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)

# Title
pdf.cell(0, 10, text="University Timetable (Monday to Friday, 2-hour Sessions)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.ln(5)

# Table Header
pdf.set_font("helvetica", style='B', size=11)
pdf.cell(25, 10, "Day", border=1, align='C')
pdf.cell(30, 10, "Time", border=1, align='C')
pdf.cell(40, 10, "Class", border=1, align='C')
pdf.cell(30, 10, "Groups", border=1, align='C')
pdf.cell(20, 10, "Students", border=1, align='C')
pdf.cell(25, 10, "Room", border=1, align='C')
pdf.cell(30, 10, "Professor", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

pdf.set_font("helvetica", size=10)

# Table Rows
if solution:
    sorted_schedule = sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1]))
    for cls, (day, time, room) in sorted_schedule:
        groups = ', '.join(class_group_mapping[cls])  # List groups separated by commas
        students = sum(student_groups[group] for group in class_group_mapping[cls])  # Total students in all groups
        prof = instructor_assignments[cls]
        
        pdf.cell(25, 10, day, border=1, align='C')
        pdf.cell(30, 10, time, border=1, align='C')
        pdf.cell(40, 10, cls, border=1, align='C')
        pdf.cell(30, 10, groups, border=1, align='C')
        pdf.cell(20, 10, str(students), border=1, align='C')
        pdf.cell(25, 10, room, border=1, align='C')
        pdf.cell(30, 10, prof, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    output_path = "/home/hamisi/Documents/projects/fypFlaskBackend/university_full_timetable_multiple_groups.pdf"
    pdf.output(output_path)
else:
    pdf.cell(0, 10, "No valid timetable found.", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    output_path = "/home/hamisi/Documents/projects/fypFlaskBackend/university_full_timetable_no_solution.pdf"
    pdf.output(output_path)

print(f"PDF generated: {output_path}")
