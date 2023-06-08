from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()


# Модель SQLAlchemy
class StudentDB(Base):
    __tablename__ = "Студент"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ФИО = Column(String(200), index=True)
    Группаid = Column(Integer, index=True)
    УчебныйПланid = Column(Integer, index=True)


class TeacherDB(Base):
    __tablename__ = "Преподаватель"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ФИО = Column(String(200), index=True)
    Факультетid = Column(Integer, index=True)


class CourseDB(Base):
    __tablename__ = "Курс"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Название = Column(String(200), index=True)
    Программа_курсаid = Column(Integer, index=True)


class GradeDB(Base):
    __tablename__ = "Оценка"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Студентid = Column(Integer, ForeignKey("Студент.id"))
    Курсid = Column(Integer, ForeignKey("Курс.id"))
    Оценка = Column(Integer, index=True)


# Модель Pydantic
class Student(BaseModel):
    id: int
    ФИО: str
    Группаid: int
    УчебныйПланid: int

    class Config:
        orm_mode = True


class Teacher(BaseModel):
    id: int
    ФИО: str
    Факультетid: int

    class Config:
        orm_mode = True


class Course(BaseModel):
    id: int
    Название: str
    Программа_курсаid: int

    class Config:
        orm_mode = True


class Grade(BaseModel):
    id: int
    Студентid: int
    Курсid: int
    Оценка: int

    class Config:
        orm_mode = True
