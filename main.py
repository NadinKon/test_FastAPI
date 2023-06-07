from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Student, StudentDB, Teacher, TeacherDB, Course, CourseDB, Grade, GradeDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "postgresql://user:*FFGHh658!@localhost:5432/db"
#DATABASE_URI = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students", response_model=Student)
def create_student(student: Student, db: Session = Depends(get_db)):
    db_student = StudentDB(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.ID == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.ID == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.ID == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    db.delete(db_student)
    db.commit()
    return {"detail": f"Студент с ID={student_id} был удален"}


@app.get("/teachers", response_model=List[Teacher])
def read_teachers(db: Session = Depends(get_db)):
    return db.query(TeacherDB).all()


@app.post("/courses", response_model=Course)
def create_course(course: Course, db: Session = Depends(get_db)):
    db_course = CourseDB(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(CourseDB).filter(CourseDB.ID == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return db_course


@app.get("/courses/{course_id}/students", response_model=List[Student])
def read_students_of_course(course_id: int, db: Session = Depends(get_db)):
    db_students = db.query(StudentDB).filter(GradeDB.КурсID == course_id).all()
    if not db_students:
        raise HTTPException(status_code=404, detail="Студенты для этого курса не найдены")
    return db_students


@app.post("/grades", response_model=Grade)
def create_grade(grade: Grade, db: Session = Depends(get_db)):
    db_grade = GradeDB(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@app.put("/grades/{grade_id}", response_model=Grade)
def update_grade(grade_id: int, grade: Grade, db: Session = Depends(get_db)):
    db_grade = db.query(GradeDB).filter(GradeDB.ID == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Оценка не найдена")

    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    db.commit()
    db.refresh(db_grade)
    return db_grade
