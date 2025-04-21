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

# Assign each subject to a group
class_group_mapping = {
    'Math': 'ComputerEngineering',
    'Physics': 'ElectricalEngineering',
    'Chemistry': 'ComputerEngineering',
    'Biology': 'ElectricalEngineering',
    'ComputerScience': 'ComputerEngineering',
    'English': 'BusinessStudies',
    'History': 'Law',
    'Geography': 'BusinessStudies',
    'Art': 'BusinessStudies',
    'Economics': 'BusinessStudies',
    'Philosophy': 'Law',
    'Statistics': 'ComputerEngineering',
    'Business': 'BusinessStudies',
    'Accounting': 'BusinessStudies',
    'Drama': 'BusinessStudies',
    'Sociology': 'Law',
    'Law': 'Law',
    'PoliticalScience': 'Law',
    'EnvironmentalScience': 'ElectricalEngineering',
    'Psychology': 'Law'
}

# Step 2: Generate domains with room capacity constraint
domains = {
    cls: [
        (day, slot, room) for day in days for slot in timeslots
        for room in rooms if rooms[room] >= student_groups[class_group_mapping[cls]]
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

# Step 4: Backtracking Search
def backtrack(schedule, domains):
    if len(schedule) == len(classes):
        if no_conflict(schedule) and room_availability(schedule):
            return schedule
        return None

    unassigned_class = next(cls for cls in classes if cls not in schedule)
    for value in domains[unassigned_class]:
        schedule[unassigned_class] = value
        if no_conflict(schedule) and room_availability(schedule):
            result = backtrack(schedule, domains)
            if result:
                return result
        del schedule[unassigned_class]
    return None

# Step 5: Solve
schedule = {}
solution = backtrack(schedule, domains)

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
pdf.cell(30, 10, "Group", border=1, align='C')
pdf.cell(20, 10, "Students", border=1, align='C')
pdf.cell(25, 10, "Room", border=1, align='C')
pdf.cell(30, 10, "Professor", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

pdf.set_font("helvetica", size=10)

# Table Rows
if solution:
    sorted_schedule = sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1]))
    for cls, (day, time, room) in sorted_schedule:
        group = class_group_mapping[cls]
        students = student_groups[group]
        prof = random.choice(professors)
        pdf.cell(25, 10, day, border=1)
        pdf.cell(30, 10, time, border=1)
        pdf.cell(40, 10, cls, border=1)
        pdf.cell(30, 10, group, border=1)
        pdf.cell(20, 10, str(students), border=1)
        pdf.cell(25, 10, room, border=1)
        pdf.cell(30, 10, prof, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    output_path = "/home/hamisi/Documents/projects/fypFlaskBackend/university_full_timetable.pdf"
    pdf.output(output_path)
else:
    pdf.cell(0, 10, text="No valid timetable found.", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    output_path = "/home/hamisi/Documents/projects/fypFlaskBackend/university_full_timetable_no_solution.pdf"
    pdf.output(output_path)

print(f"PDF generated: {output_path}")