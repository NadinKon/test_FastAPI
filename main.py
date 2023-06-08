from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Student, StudentDB, Teacher, TeacherDB, Course, CourseDB, Grade, GradeDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "postgresql://postgres:*FFGHh658!@localhost:5432/db"
# DATABASE_URI = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# функция для создания и управления сессией базы данных
def get_db():
    db = SessionLocal()  # создание экземпляра сессии
    try:
        yield db  # предоставление экземпляра сессии внешнему коду
    finally:
        db.close()  # закрытие сессии


# Маршрут для создания студента в базе данных
@app.post("/students", response_model=Student)
def create_student(student: Student, db: Session = Depends(get_db)):  # обработка запроса и создания нового студента
    db_student = StudentDB(**student.dict())  # создание объекта студента SQLAlchemy из объекта Pydantic
    db.add(db_student)  # добавление нового объекта студента в сессию SQLAlchemy
    db.commit()  # сохранение изменений в базе данных
    db.refresh(db_student)  # обновление объекта студента с полученными данными из базы данных
    return Student(**db_student.__dict__)


# Маршрут для получения информации о студенте по его id
@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):  # обработка запроса и получения данных студента
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()  # поиск студента в базе данных по id
    if db_student is None:  # исключения, если студент не найден
        raise HTTPException(status_code=404, detail="Студент не найден")
    return Student(**db_student.__dict__)


# Маршрут для обновления информации о студенте по его id
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):  # обновления информации о студент
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()  # поиск студента в базе данных по id
    if db_student is None:  # исключения, если студент не найден
        raise HTTPException(status_code=404, detail="Студент не найден")
    # Для каждого поля в объекте студента, обновить соответствующее поле в базе данных
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()  # сохранение изменений в базе данных
    db.refresh(db_student)  # обновление объекта студента с полученными данными из базы данных
    return Student(**db_student.__dict__)


# Маршрут для удаления студента по его id
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):  # обработка запроса и удаления студента
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()  # поиск студента в базе данных по id
    if db_student is None:  # исключения, если студент не найден
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.delete(db_student)  # удаление объекта студента из сессии SQLAlchemy
    db.commit()  # сохранение изменений в базе данных
    # Возвращение ответа, подтверждающего успешное удаление студента
    return {"detail": f"Студент с ID={student_id} был удален"}


# Маршрут для получения списка всех преподавателей
@app.get("/teachers", response_model=List[Teacher])
def read_teachers(db: Session = Depends(get_db)):  # обработка запроса и получения списка всех преподавателей
    db_teachers = db.query(TeacherDB).all()  # запрос всех преподавателей из базы данных
    return [Teacher(**teacher.__dict__) for teacher in db_teachers]


# Маршрут для создания нового курса
@app.post("/courses", response_model=Course)
def create_course(course: Course, db: Session = Depends(get_db)):  # обработка запроса и создания нового курса
    db_course = CourseDB(**course.dict())  # создание объекта курса в формате SQLAlchemy модели из входного объекта Pydantic модели
    db.add(db_course)  # добавление нового курса в сессию SQLAlchemy
    db.commit()  # сохранение изменений в базе данных
    db.refresh(db_course)  # обновление объекта курса с полученными данными из базы данных
    return Course(**db_course.__dict__)


# Маршрут для чтения определенного курса по ID
@app.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):  # обработка запроса и чтения определенного курса
    db_course = db.query(CourseDB).filter(CourseDB.id == course_id).first()  # запрос курса из базы данных по ID
    if db_course is None:
        raise HTTPException(status_code=404, detail="Курс не найден")  # если курс не найден, исключение
    return Course(**db_course.__dict__)


# Маршрут для чтения студентов определенного курса
@app.get("/courses/{course_id}/students", response_model=List[Student])
def read_students_of_course(course_id: int, db: Session = Depends(get_db)):  # обработка запроса и чтения студентов курса
    # Запрос студентов из базы данных, которые присоединены к курсу с указанным ID
    db_students = db.query(StudentDB).join(GradeDB, GradeDB.Студентid == StudentDB.id).filter(GradeDB.Курсid == course_id).all()
    if not db_students:  # исключения, если студент не найден
        raise HTTPException(status_code=404, detail="Студенты для этого курса не найдены")
    return [Student.from_orm(db_student) for db_student in db_students]


# Маршрут для создания новой оценки
@app.post("/grades", response_model=Grade)
def create_grade(grade: Grade, db: Session = Depends(get_db)):  # обработка запроса и создания новой оценки
    db_grade = GradeDB(**grade.dict())  # создание объекта оценки в формате SQLAlchemy модели из входного объекта Pydantic модели
    db.add(db_grade)  # добавление новой оценки в сессию SQLAlchemy
    db.commit()  # сохранение изменений в базе данных
    db.refresh(db_grade)  # обновление объекта оценки с полученными данными из базы данных
    return Grade(**db_grade.__dict__)


# Маршрут для обновления оценки
@app.put("/grades/{grade_id}", response_model=Grade)
def update_grade(grade_id: int, grade: Grade, db: Session = Depends(get_db)):  # обработка запроса и обновления оценки
    db_grade = db.query(GradeDB).filter(GradeDB.id == grade_id).first()  # запрос оценки из базы данных по указанному ID
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Оценка не найдена")  # Если оценка не найдена, исключение 404
    # Обновление полей объекта оценки значениями из входного объекта Pydantic модели
    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    db.commit()  # сохранение изменений в базе данных
    db.refresh(db_grade)  # обновление объекта оценки с полученными данными из базы данных
    return Grade(**db_grade.__dict__)
