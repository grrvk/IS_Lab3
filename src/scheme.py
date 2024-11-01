class Group:
    def __init__(self, group_name, number_of_students, subgroups):
        self.group_name = group_name
        self.number_of_students = number_of_students
        self.subgroups = [sub for sub in subgroups.split(';')] if subgroups else None

    def __repr__(self):
        return f"Group: {self.group_name}, {self.number_of_students}, {self.subgroups}"


class Teacher:
    def __init__(self, name, subjects_taught, subject_type, maxHoursPerWeek):
        self.name = name
        self.subjects_taught = subjects_taught if subjects_taught else None
        self.subject_type = subject_type
        self.maxHoursPerWeek = maxHoursPerWeek

    def __repr__(self):
        return f"Teacher {self.name}: {self.subjects_taught}, {self.subject_type}, {self.maxHoursPerWeek}"


class Auditorium:
    def __init__(self, auditorium_name, capacity):
        self.auditorium_name = auditorium_name
        self.capacity = capacity

    def __repr__(self):
        return f"Auditorium {self.auditorium_name}, {self.capacity}"


class Subject:
    def __init__(self, subject_name, group, lectures_number, practice_number,
                 requires_subgroups, week):
        self.subject_name = subject_name
        self.group = group
        self.lectures_number = lectures_number
        self.practice_number = practice_number
        self.requires_subgroups = bool(requires_subgroups)
        self.week = week

    def __repr__(self):
        return (f"Subject {self.subject_name}, {self.group}, {self.lectures_number}, "
                f"{self.practice_number}, {self.requires_subgroups}, {self.week}")


class Lesson:
    def __init__(self, subject, subject_type, group, subgroup=None):
        self.subject = subject
        self.subject_type = subject_type
        self.group = group
        self.subgroup = subgroup

        self.time = None
        self.teacher = None
        self.auditorium = None


class Schedule:
    def __init__(self, slots):
        self.timetable = {time_slot: [] for time_slot in slots}
        self.numOfConflicts = 0
        self.fitness = -1

    def initialize(self, subjects, auditoriums, teachers, groups):
        pass




