import pandas as pd

from database.scheme import engine, session, Auditorium, Group, Teacher, Subject, TeacherSubject


def read_base(scheme):
    sql_statement = session.query(scheme).statement
    df = pd.read_sql(sql=sql_statement, con=engine)
    return df


df_groups = read_base(Group)
df_teachers = read_base(Teacher)
df_subjects = read_base(Subject)
df_auditorium = read_base(Auditorium)
df_teacher_subject = read_base(TeacherSubject)