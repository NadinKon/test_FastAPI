from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()


# Модель SQLAlchemy
class StudentDB(Base):
    __tablename__ = "Студент"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ФИО = Column(String(200), index=True)
    ГруппаID = Column(Integer, index=True)
    УчебныйПланID = Column(Integer, index=True)

class TeacherDB(Base):
    __tablename__ = "Преподаватель"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ФИО = Column(String(200), index=True)
    ФакультетID = Column(Integer, index=True)

class CourseDB(Base):
    __tablename__ = "Курс"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Название = Column(String(200), index=True)
    Программа_курсаID = Column(Integer, index=True)

class GradeDB(Base):
    __tablename__ = "Оценка"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    СтудентID = Column(Integer, ForeignKey("Студент.ID"))
    КурсID = Column(Integer, ForeignKey("Курс.ID"))
    Оценка = Column(Integer, index=True)


# Модель Pydantic
class Student(BaseModel):
    ID: int
    ФИО: str
    ГруппаID: int
    УчебныйПланID: int

class Teacher(BaseModel):
    ID: int
    ФИО: str
    ФакультетID: int

class Course(BaseModel):
    ID: int
    Название: str
    Программа_курсаID: int

class Grade(BaseModel):
    ID: int
    СтудентID: int
    КурсID: int
    Оценка: int

