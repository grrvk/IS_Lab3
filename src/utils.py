from scheme import Group, Teacher, Auditorium, Subject
from database.database_query import df_groups, df_teachers, df_subjects, df_auditorium, df_teacher_subject


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


def read_subjects(df=df_subjects, extra_df=df_groups):
    subjects = []
    for index, row in df.iterrows():
        group = extra_df[extra_df['group_id'] == row['group_id']]['group_name'].values[0]
        subjects.append(Subject(subject_name=row['subject_name'],
                                group=group,
                                lectures_number=row['lectures_number'],
                                practice_number=row['practice_number'],
                                requires_subgroups=row['requires_subgroups'],
                                week=row['week']))

    return subjects


# groups = read_groups()
# auditoriums = read_auditoriums()
# teachers = read_teachers()
# subjects = read_subjects()
#
# #print(groups)
# #print(auditoriums)
# print(teachers)
# #print(subjects)
