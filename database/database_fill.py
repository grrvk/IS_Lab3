import random
from sqlalchemy import select

from scheme import session, Auditorium, Group, Teacher, Subject, TeacherSubject

tables = [Auditorium, Group, Teacher, Subject, TeacherSubject]

for table in tables:
    session.query(table).delete()
    session.commit()

auditorium_capacities = [60]

group_names = ['TTP-41', 'TTP-42', 'MI-41', 'MI-42', 'TK-4']
group_capacities = [25, 28, 30]
group_subgroups = ['1;2']

teacher_names = ['Пашко', 'Вергунова', 'Бобиль', 'Закала', 'Зінько', 'Мащенко', 'Тарануха',
                 'Федорус', 'Мисечко', 'Ткаченко', 'Терещенко', 'Свистунов', 'Красовська',
                 'Шишацька', 'Дорошенко', 'Крак', 'Чернега', 'Злотник', 'Башняков', 'Коробова',
                 'Коваль', 'Криволап', 'Галавай', 'Башук']
teacher_subject_types = ['Практика', 'Лекція', 'Обидва']
teacher_maxHoursPerWeek = [22.5]

subject_names = ['Статистичне моделювання', 'Інтелектуальні системи', 'Теорія прийняття рішень',
                 'Інформаційні технології', 'Складність алгоритмів', 'Основи комп\'ютерної лінгвістики',
                 'Проблеми штучного інтелекту']
lectures_number = [4, 5, 6]
practice_number = [3, 4]
subjects_weeks = ['Парний', 'Непарний', 'Обидва']


AUDITORIUMS_NUM = len(subject_names)
TEACHERS_NUM = len(teacher_names)
GROUPS_NUM = len(group_names)


for i in range(1, AUDITORIUMS_NUM+1):
    aud = Auditorium(auditorium_name=f"A{i}", capacity=random.choice(auditorium_capacities))
    session.add(aud)

for i in range(GROUPS_NUM):
    grp = Group(group_name=group_names[i],
                number_of_students=random.choice(group_capacities),
                subgroups=random.choice(group_subgroups))
    session.add(grp)

session.commit()

SUBJECT_RATE = 1
random.shuffle(group_names)
for group_name in group_names:
    subject_amount = int(len(subject_names) * SUBJECT_RATE)
    random.shuffle(subject_names)
    selected_subjects = subject_names[:subject_amount]
    for subject in selected_subjects:
        stmt = select(Group).where(Group.group_name == group_name)
        group = session.scalars(stmt).one()
        sbj = Subject(subject_name=subject, group_name=group.group_name,
                      lectures_number=random.choice(lectures_number),
                      practice_number=random.choice(practice_number),
                      requires_subgroups=random.choices([True, False], weights=[0.4, 0.6], k=1)[0],
                      week=random.choices(subjects_weeks, weights=[0.2, 0.2, 0.6], k=1)[0])
        session.add(sbj)

session.commit()

random.shuffle(teacher_names)

for i in range(TEACHERS_NUM):
    teacher = Teacher(name=teacher_names[i], subject_type=random.choice(teacher_subject_types),
                      maxHoursPerWeek=random.choice(teacher_maxHoursPerWeek))
    session.add(teacher)

session.commit()

teachers_queried = session.scalars(select(Teacher)).all()
for subject_name in subject_names:
    random_teacher = random.choice(teachers_queried)
    teacher_subject = TeacherSubject(teacher_name=random_teacher.name,
                                     subject_name=subject_name)
    session.add(teacher_subject)
    if random_teacher.subject_type in ['Лекція', 'Практика']:
        filtered_types = [t for t in teacher_subject_types if t != random_teacher.subject_type]
        filtered_teachers = [t for t in teachers_queried if t.subject_type
                             in filtered_types]
        second_random_teacher = random.choice(filtered_teachers)
        second_teacher_subject = TeacherSubject(teacher_name=second_random_teacher.name,
                                                subject_name=subject_name)
        session.add(second_teacher_subject)

session.commit()

teacher_subjects_queried = session.scalars(select(TeacherSubject)).all()
teacher_subjects_names = set([t.teacher_name for t in teacher_subjects_queried])
unoccupied_teachers = [t for t in teacher_names if t not in teacher_subjects_names]

while len(unoccupied_teachers) != 0:
    random_teacher = random.choice(unoccupied_teachers)
    stmt = select(Teacher).where(Teacher.name == random_teacher)
    teacher = session.scalars(stmt).one()

    random_subject = random.choice(subject_names)
    teacher_subject = TeacherSubject(teacher_name=teacher.name,
                                     subject_name=random_subject)
    session.add(teacher_subject)
    unoccupied_teachers.remove(random_teacher)

session.commit()

