import random
from sqlalchemy import select, update

from scheme import session, Auditorium, Group, Teacher, Subject, TeacherSubject

tables = [Auditorium, Group, Teacher, Subject, TeacherSubject]

for table in tables:
    session.query(table).delete()
    session.commit()

auditorium_capacities = [60]

group_names = ['TTP-41', 'TTP-42', 'MI-41', 'MI-42', 'TK-4']
group_capacities = [25, 28, 30]
group_subgroups = ['1;2']

teacher_names = ['Зінько Т.П.', 'Пашко А.О.', 'Тарануха В.Ю.', 'Ткаченко О.М.', 'Вергунова І.В.']
teacher_subject_types = ['Практика', 'Лекція', 'Обидва']
teacher_maxHoursPerWeek = [10, 20]

subject_names = ['Статистичне моделювання', 'Інтелектуальні системи', 'Теорія прийняття рішень',
                 'Інформаційні технології', 'Складність алгоритмів']
lectures_number = [6, 9]
practice_number = [4, 7]
subjects_weeks = ['Парний', 'Непарний', 'Обидва']


AUDITORIUMS_NUM = 6
TEACHERS_NUM = len(teacher_names)
GROUPS_NUM = len(group_names)
SUBJECTS_NUM = 10

assert SUBJECTS_NUM >= GROUPS_NUM
assert TEACHERS_NUM == len(subject_names)
assert SUBJECTS_NUM <= len(subject_names)*len(teacher_names)

for i in range(1, AUDITORIUMS_NUM+1):
    aud = Auditorium(auditorium_name=f"A{i}", capacity=random.choice(auditorium_capacities))
    session.add(aud)

for i in range(GROUPS_NUM):
    grp = Group(group_name=group_names[i],
                number_of_students=random.choice(group_capacities),
                subgroups=random.choice(group_subgroups))
    session.add(grp)

session.commit()

random.shuffle(group_names)
random.shuffle(subject_names)
unused_subjects = [s for s in subject_names if s not in subject_names[:len(group_names)]]
initial_pairs = [(subject_names[i], group_names[i]) for i in range(len(group_names))]

additional_pairs = []
for s in unused_subjects:
    additional_pairs.append((s, random.choice(group_names)))
while len(initial_pairs) + len(additional_pairs) < SUBJECTS_NUM+1:
    pair = (random.choice(subject_names), random.choice(group_names))
    while pair in initial_pairs or pair in additional_pairs:
        pair = (random.choice(subject_names), random.choice(group_names))
    additional_pairs.append(pair)
full_pairs = initial_pairs + additional_pairs

for pair in full_pairs:
    stmt = select(Group).where(Group.group_name == pair[1])
    group = session.scalars(stmt).one()
    sbj = Subject(subject_name=pair[0], group_name=group.group_name,
                  lectures_number=random.choice(lectures_number),
                  practice_number=random.choice(practice_number),
                  requires_subgroups=random.choice([True, False]),
                  week=random.choice(subjects_weeks))
    session.add(sbj)

session.commit()

random.shuffle(teacher_names)

#subjects_queried = session.scalars(select(Subject).where(Subject.teacher_assigned == False)).all()
for i in range(TEACHERS_NUM):
    teacher = Teacher(name=teacher_names[i], subject_type=random.choice(teacher_subject_types),
                      maxHoursPerWeek=random.choice(teacher_maxHoursPerWeek))

    # number_of_subjects = random.randint(1, 3)
    # for i in range (number_of_subjects):
    #     random_subject = random.choice(subjects_queried)
    #     session.execute(update(Subject).where(Subject.subject_id == random_subject.subject_id).values(teacher_assigned=True))
    #     teacher.subjects_taught.append(random_subject)
    #     subjects_queried.remove(random_subject)
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

# while len(subjects_queried) != 0:
#     random_teacher = random.choice(teachers_queried)
#     random_subject = random.choice(subjects_queried)
#     session.execute(update(Subject).where(Subject.subject_id == random_subject.subject_id).values(teacher_assigned=True))
#     random_teacher.subjects_taught.append(random_subject)
#     subjects_queried.remove(random_subject)


session.commit()

