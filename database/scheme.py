from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from typing import List, Optional

import random

import os
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()


# association_table = Table(
#     "teacher_subject",
#     Base.metadata,
#     Column("teacher_name", String, ForeignKey("teacher.name")),
#     Column("subject_name", String, ForeignKey("subject.subject_name"))
# )


class Group(Base):
    __tablename__ = 'group'

    group_id = Column("group_id", Integer, primary_key=True, autoincrement=True)
    group_name = Column("group_name", String)
    number_of_students = Column("number_of_students", Integer)
    subgroups = Column("subgroups", String)

    def __init__(self, group_name, number_of_students, subgroups):
        self.group_name = group_name
        self.number_of_students = number_of_students
        self.subgroups = subgroups

    def __repr__(self):
        return (f"Group(id={self.group_id!r}, group_name={self.group_name!r},"
                f"number_of_students={self.number_of_students!r}, "
                f"subgroups={self.subgroups!r})")


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column("subject_id", Integer, primary_key=True, autoincrement=True)
    subject_name = Column("subject_name", String)
    group_id = Column("group_id", Integer, ForeignKey('group.group_id'), nullable=False)
    lectures_number = Column("lectures_number", Integer)
    practice_number = Column("practice_number", Integer)
    requires_subgroups = Column("requires_subgroups", Boolean)
    week = Column("week", String)

    teacher_assigned = Column("teacher_assigned", Boolean)

    def __init__(self, subject_name, group_id, lectures_number, practice_number,
                 requires_subgroups, week, teacher_assigned=False):
        self.subject_name = subject_name
        self.group_id = group_id
        self.lectures_number = lectures_number
        self.practice_number = practice_number
        self.requires_subgroups = bool(requires_subgroups)
        self.week = week
        self.teacher_assigned = bool(teacher_assigned)

    def __repr__(self):
        return (f"Subject {self.subject_name}, {self.group_id}, {self.lectures_number}, "
                f"{self.practice_number}, {self.requires_subgroups}, {self.week}, "
                f"{self.teacher_assigned})")


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column("teacher_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    subject_type = Column("subject_type", String)
    maxHoursPerWeek = Column("maxHoursPerWeek", Integer)

    #subjects_taught: Mapped[List[Subject]] = relationship(secondary=association_table)

    def __init__(self, name, subject_type, maxHoursPerWeek):
        self.name = name
        self.subject_type = subject_type
        self.maxHoursPerWeek = maxHoursPerWeek


class Auditorium(Base):
    __tablename__ = 'auditorium'

    auditorium_id = Column("auditorium_id", Integer, primary_key=True, autoincrement=True)
    auditorium_name = Column("auditorium_name", String)
    capacity = Column("capacity", Integer)

    def __init__(self, auditorium_name, capacity):
        self.auditorium_name = auditorium_name
        self.capacity = capacity


class TeacherSubject(Base):
    __tablename__ = 'teacher_subject'

    teacher_subject_id = Column("teacher_subject_id", Integer, primary_key=True, autoincrement=True)
    teacher_name = Column("teacher_name", String, ForeignKey('teacher.name'), nullable=False)
    subject_name = Column("subject_name", String)

    def __init__(self, teacher_name, subject_name):
        self.teacher_name = teacher_name
        self.subject_name = subject_name


engine = create_engine('sqlite:///database.sqlite', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

