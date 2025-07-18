from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate

router = APIRouter()

@router.post("/save")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this email already exists.")

    new_student = Student(name=student.name, email=student.email, major=student.major)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "id": new_student.id,
        "name": new_student.name,
        "email": new_student.email,
        "major": new_student.major
    }

@router.get("/all")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "major": s.major
        }
        for s in students
    ]
