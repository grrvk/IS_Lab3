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

        self.occupied_hours = 0

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

    def __repr__(self):
        return (f"Lesson {self.subject}, {self.subject_type}, {self.group}, {self.subgroup}, "
                f"{self.time}, {self.auditorium}, {self.teacher}")


DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


class Schedule:
    def __init__(self, slots):
        self.timetable = {time_slot: [] for time_slot in slots}
        self.numOfConflicts = 0
        self.fitness = -1

    def get_schedule_teachers(self):
        teachers = []
        for time_slot in self.timetable:
            lessons = self.timetable[time_slot]
            for lesson in lessons:
                teachers.append(lesson.teacher)
        return list(set(teachers))

    def get_schedule_groups(self):
        groups = []
        for time_slot in self.timetable:
            lessons = self.timetable[time_slot]
            for lesson in lessons:
                groups.append(lesson.group.group_name)
        return list(set(groups))

    def calculate_fitness(self):
        schedule_teachers = self.get_schedule_teachers()
        schedule_groups = self.get_schedule_groups()

        teacher_schedule = {teacher.name: [] for teacher in schedule_teachers}
        group_schedule = {group_name: [] for group_name in schedule_groups}

        for time_slot in self.timetable:
            lessons = self.timetable[time_slot]
            if len(lessons) == 0:
                self.numOfConflicts += 200
            else:
                used_auditoriums = []
                occupied_teachers = []
                occupied_groups = []

                for lesson in lessons:
                    groupNumOfStudents = lesson.group.number_of_students if lesson.subgroup is None \
                        else lesson.group.number_of_students // 2
                    if groupNumOfStudents > lesson.auditorium.capacity:  # auditorium capacity check
                        self.numOfConflicts += 1

                    if lesson.auditorium.auditorium_name in used_auditoriums:  # auditorium usage check
                        self.numOfConflicts += 2
                    else:
                        used_auditoriums.append(lesson.auditorium.auditorium_name)

                    if lesson.subject.subject_name not in lesson.teacher.subjects_taught \
                        or not (lesson.subject_type == lesson.teacher.subject_type
                                or lesson.teacher.subject_type == 'Обидва'):  # lesson-teacher compatibility check
                        self.numOfConflicts += 1

                    teacher_week_name = f"{lesson.teacher.name}_{lesson.subject.week}"
                    teacher_both_name = f"{lesson.teacher.name}_Обидва"
                    if teacher_week_name in occupied_teachers or teacher_both_name in occupied_teachers:  # teacher occupied check
                        self.numOfConflicts += 2
                    else:
                        occupied_teachers.append(teacher_week_name)
                        pair = (time_slot, lesson.subject.week)
                        teacher_schedule[lesson.teacher.name].append(pair)

                    group_week_name = f"{lesson.group.group_name}_{lesson.subject.week}"
                    group_both_name = f"{lesson.group.group_name}_Обидва"
                    if lesson.subgroup is not None:  # subgroup/group occupied check
                        subgroup_week_name = f"{lesson.subgroup}_{lesson.subject.week}"
                        subgroup_both_name = f"{lesson.subgroup}_Обидва"
                        if (subgroup_week_name in occupied_groups or subgroup_both_name in occupied_groups
                                or group_week_name in occupied_groups or group_both_name in occupied_groups):
                            self.numOfConflicts += 2
                        else:
                            occupied_groups.append(subgroup_week_name)
                            triple = (time_slot, 'Обидва', lesson.subject.week)
                            group_schedule[lesson.group.group_name].append(triple)
                    else:
                        if group_week_name in occupied_groups or group_both_name in occupied_groups:
                            self.numOfConflicts += 2
                        else:
                            occupied_groups.append(group_week_name)
                            triple = (time_slot, lesson.subgroup, lesson.subject.week)
                            group_schedule[lesson.group.group_name].append(triple)

        for teacher in schedule_teachers:
            if teacher.occupied_hours > teacher.maxHoursPerWeek:
                self.numOfConflicts += 1

        for group_name, schedule_list in group_schedule.items():
            schedule_sorted = sorted(schedule_list, key=lambda x: (DAYS.index(x[0][0]), int(x[0][1])))

            weeks_check = ['Парний', 'Непарний']
            for week_type in weeks_check:
                week_schedule = [entry for entry in schedule_sorted if (entry[2] in [week_type, 'Обидва'])]
                for i in range(len(week_schedule) - 1):
                    day1, subgroup1, week1 = schedule_sorted[i]
                    day2, subgroup2, week2 = schedule_sorted[i + 1]
                    if day1[0] == day2[0]:
                        gaps = int(day1[1]) - int(day2[1]) - 1
                        if gaps > 0:
                            self.numOfConflicts += gaps
                            print(f"Penalty: Gaps in group {group_name} schedule on {day1[0]} between periods {day1[1]} and {day2[1]}")

        for teacher_name, schedule_list in teacher_schedule.items():
            schedule_sorted = sorted(schedule_list, key=lambda x: (DAYS.index(x[0][0]), int(x[0][1])))

            weeks_check = ['Парний', 'Непарний']
            for week_type in weeks_check:
                week_schedule = [entry for entry in schedule_sorted if (entry[1] in [week_type, 'Обидва'])]
                for i in range(len(week_schedule) - 1):
                    day1, week1 = schedule_sorted[i]
                    day2, week2 = schedule_sorted[i + 1]
                    if day1[0] == day2[0]:
                        gaps = int(day1[1]) - int(day2[1]) - 1
                        if gaps > 0:
                            self.numOfConflicts += gaps
                            print(f"Penalty: Gaps in teachers {teacher_name} schedule on {day1[0]} between periods {day1[1]} and {day2[1]}")
        self.fitness = 1 / (1.0 * self.numOfConflicts + 1)







