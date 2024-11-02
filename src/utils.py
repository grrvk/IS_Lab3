import os
import pandas as pd

from scheme import Group, Teacher, Auditorium, Subject
from database.database_query import df_groups, df_teachers, df_subjects, df_auditorium, df_teacher_subject

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


def read_groups(df=df_groups):
    groups = []
    for index, row in df.iterrows():
        groups.append(Group(group_name=row['group_name'],
                            number_of_students=row['number_of_students'],
                            subgroups=row['subgroups']))
    return groups


def read_auditoriums(df=df_auditorium):
    auditoriums = []
    for index, row in df.iterrows():
        auditoriums.append(Auditorium(auditorium_name=row['auditorium_name'],
                                      capacity=row['capacity']))
    return auditoriums


def read_teachers(df=df_teachers, extra_df=df_teacher_subject):
    teachers = []
    for index, row in df.iterrows():
        subjects_taught = extra_df[extra_df['teacher_name'] == row['name']]['subject_name'].values.tolist()
        teachers.append(Teacher(name=row['name'],
                                subjects_taught=subjects_taught,
                                subject_type=row['subject_type'],
                                maxHoursPerWeek=row['maxHoursPerWeek']))

    return teachers


def read_subjects(groups_list, df=df_subjects):
    subjects = []
    for index, row in df.iterrows():
        group = next((g for g in groups_list if g.group_name == row['group_name']), None)
        subjects.append(Subject(subject_name=row['subject_name'],
                                group=group,
                                lectures_number=row['lectures_number'],
                                practice_number=row['practice_number'],
                                requires_subgroups=row['requires_subgroups'],
                                week=row['week']))

    return subjects


corresponding_time = ['8:40-10:15', '10:35-12:10', '12:20-13:55']


def exportSchedule(schedule, dir='schedules'):
    os.makedirs(dir, exist_ok=True)
    week_types = ['Парний', 'Непарний']

    for week in week_types:
        csv_file_path = f'{dir}/{week}.csv'
        df = pd.DataFrame(columns=['Day', 'Subject', 'Teacher', 'Group', 'Auditorium', 'Time'])

        for time_slot in schedule.timetable:
            lessons = schedule.timetable[time_slot]
            for lesson in lessons:
                if lesson.subject.week == week or lesson.subject.week == 'Обидва':
                    df.loc[len(df.index)] = [time_slot[0], lesson.subject.subject_name, lesson.teacher.name,
                                             lesson.group.group_name, lesson.auditorium.auditorium_name,
                                             corresponding_time[int(time_slot[1])-1]]
        df.to_csv(csv_file_path, index=False)




