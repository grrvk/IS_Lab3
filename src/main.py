import random

from src.utils import read_groups, read_teachers, read_auditoriums, read_subjects
from src.scheme import Lesson, Schedule

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
PERIODS = ['8:40-10:15', '10:35-12:10', '12:20-13:55']
TIME_SLOTS = [(day, period) for day in DAYS for period in PERIODS]

auditoriums = read_auditoriums()
groups = read_groups()
teachers = read_teachers()
subjects = read_subjects()

print(subjects[0])


def generatePopulation():
    schedule = Schedule(TIME_SLOTS)
    for subject in subjects:
        for _ in range(subject.lectures_number):
            group = next((g for g in groups if g.group_name == subject.group_name), None)
            lesson = Lesson(subject=subject,
                            subject_type='Лекція',
                            group=group)
            randomAssignment(lesson=lesson, schedule=schedule)
        for _ in range(subject.practice_number):
            group = next((g for g in groups if g.group_name == subject.group_name), None)
            lesson = Lesson(subject=subject,
                            subject_type='Практика',
                            group=group)
            randomAssignment(lesson=lesson, schedule=schedule)


def randomAssignment(lesson: Lesson, schedule):
    time_slot = random.choice(TIME_SLOTS)
    auditorium = random.choice(auditoriums)
    available_teachers = [t for t in teachers if lesson.subject.subject_name in t.subjects_taught
                          and (lesson.subject_type == t.subject_type or t.subject_type == 'Обидва')]

    random_teacher = random.choice(available_teachers)
    lesson.time = time_slot
    lesson.teacher = random_teacher
    lesson.auditorium = auditorium

    schedule.timetable[time_slot].append(lesson)

# print(groups)
# print(teachers)
# print(subjects)
# print(auditoriums)
