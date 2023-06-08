from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()


# Модель SQLAlchemy для таблицы "Студент"
class StudentDB(Base):
    __tablename__ = "Студент"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # идентификатор студента
    ФИО = Column(String(200), index=True)  # имя студента
    Группаid = Column(Integer, index=True)  # идентификатор группы студента
    УчебныйПланid = Column(Integer, index=True)  # идентификатор учебного плана студента


# Модель SQLAlchemy для таблицы "Преподаватель"
class TeacherDB(Base):
    __tablename__ = "Преподаватель"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # идентификатор преподавателя
    ФИО = Column(String(200), index=True)  # имя преподавателя
    Факультетid = Column(Integer, index=True)  # идентификатор факультета преподавателя


# Модель SQLAlchemy для таблицы "Курс"
class CourseDB(Base):
    __tablename__ = "Курс"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # идентификатор курса
    Название = Column(String(200), index=True)  # название курса
    Программа_курсаid = Column(Integer, index=True)  # идентификатор программы курса


# Модель SQLAlchemy для таблицы "Оценка"
class GradeDB(Base):
    __tablename__ = "Оценка"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # идентификатор оценки
    Студентid = Column(Integer, ForeignKey("Студент.id"))  # идентификатор студента
    Курсid = Column(Integer, ForeignKey("Курс.id"))  # идентификатор курса
    Оценка = Column(Integer, index=True)  # оценка студента


# Модель Pydantic для студента
class Student(BaseModel):
    id: int  # идентификатор студента
    ФИО: str  # имя студента
    Группаid: int  # идентификатор группы студента
    УчебныйПланid: int  # идентификатор учебного плана студента

    class Config:
        orm_mode = True  # режим ORM для корректной работы с SQLAlchemy


# Модель Pydantic для преподавателя
class Teacher(BaseModel):
    id: int  # идентификатор преподавателя
    ФИО: str  # полное имя преподавателя
    Факультетid: int  # идентификатор факультета преподавателя

    class Config:
        orm_mode = True  # режим ORM для корректной работы с SQLAlchemy


# Модель Pydantic для курса
class Course(BaseModel):
    id: int  # идентификатор курса
    Название: str  # название курса
    Программа_курсаid: int  # идентификатор программы курса

    class Config:
        orm_mode = True  # режим ORM для корректной работы с SQLAlchemy


# Модель Pydantic для оценки
class Grade(BaseModel):
    id: int  # идентификатор оценки
    Студентid: int  # идентификатор студента
    Курсid: int  # идентификатор курса
    Оценка: int  # оценка студента

    class Config:
        orm_mode = True  # режим ORM для корректной работы с SQLAlchemy
