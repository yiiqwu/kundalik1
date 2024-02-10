from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI(docs_url="/")
Base = declarative_base()

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grade = Column(Integer)

class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)

class ClassModel(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class GradeModel(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    class_id = Column(Integer, index=True)
    grade = Column(Integer)

class SubjectModel(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class Student(BaseModel):
    name: str
    grade: int

class Teacher(BaseModel):
    name: str
    subject: str

class Subject(BaseModel):
    name: str

@app.post("/students/", response_model=Student)
def create_student(student: Student):
    db = SessionLocal()
    db_student = StudentModel(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db.close()
    return db_student

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    db = SessionLocal()
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    db.close()
    return db_student


class Class(BaseModel):
    name: str

class Grade(BaseModel):
    student_id: int
    class_id: int
    grade: int

@app.post("/classes/", response_model=Class)
def create_class(class_: Class):
    db = SessionLocal()
    db_class = ClassModel(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    db.close()
    return db_class

@app.get("/classes/{class_id}", response_model=Class)
def read_class(class_id: int):
    db = SessionLocal()
    db_class = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    db.close()
    return db_class

@app.post("/grades/", response_model=Grade)
def create_grade(grade: Grade):
    db = SessionLocal()
    db_grade = GradeModel(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    db.close()
    return db_grade

@app.get("/grades/{grade_id}", response_model=Grade)
def read_grade(grade_id: int):
    db = SessionLocal()
    db_grade = db.query(GradeModel).filter(GradeModel.id == grade_id).first()
    db.close()
    return db_grade

@app.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: Teacher):
    db = SessionLocal()
    db_teacher = TeacherModel(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    db.close()
    return db_teacher

@app.get("/teachers/{teacher_id}", response_model=Teacher)
def read_teacher(teacher_id: int):
    db = SessionLocal()
    db_teacher = db.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
    db.close()
    return db_teacher


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if student is not None:
        db.delete(student)
        db.commit()
    db.close()
    return {"message": "Student deleted"}

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    db = SessionLocal()
    teacher = db.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
    if teacher is not None:
        db.delete(teacher)
        db.commit()
    db.close()
    return {"message": "Teacher deleted"}

@app.delete("/grades/{grade_id}")
def delete_grade(grade_id: int):
    db = SessionLocal()
    grade = db.query(GradeModel).filter(GradeModel.id == grade_id).first()
    if grade is not None:
        db.delete(grade)
        db.commit()
    db.close()
    return {"message": "Grade deleted"}
