from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.application.usecases.create_student import CreateStudent, Input
from src.application.usecases.get_student import GetStudent
from src.application.errors.application_erros import (
    StudentAlreadyExistsError,
    InvalidInputError
)
from tests.helpers import random_enrollment_id
import pytest

student_dao = StudentDaoMongo()

def test_create_student_should_create_student_properly():
    create_student = CreateStudent(student_dao)
    enrollment_id = random_enrollment_id()
    input_create_student = Input(
        name="John Doe",
        enrollment_id=enrollment_id,
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_create_student)
    get_student = GetStudent(student_dao)
    output_get_student = get_student.execute(output_create_student.enrollment_id)
    assert output_get_student.name == "John Doe"
    assert output_get_student.age == 20
    assert output_get_student.major == "Computer Science"
    assert output_get_student.email == "johndoe@harvard.com"
    assert output_get_student.id is not None
    assert output_get_student.enrollment_id  == enrollment_id
    student_dao.remove(output_get_student.id)

def test_create_student_should_throw_error_if_student_already_exists():
    create_student = CreateStudent(student_dao)
    enrollment_id = random_enrollment_id()
    input_create_student = Input(
        name="John Doe",
        enrollment_id=enrollment_id,
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student =  create_student.execute(input_create_student)
    with pytest.raises(StudentAlreadyExistsError) as excinfo:
        create_student.execute(input_create_student)
    assert excinfo.value.args[0] == f"Student with enrollment id {enrollment_id} already exists"
    student_dao.remove(output_create_student.id)

def test_create_student_should_throw_error_if_student_email_is_invalid():
    create_student = CreateStudent(student_dao)
    enrollment_id = random_enrollment_id()
    input_create_student = Input(
        name="John Doe",
        enrollment_id=enrollment_id,
        age=20,
        major="Computer Science",
        email="johndoeharvard.com"
    )
    with pytest.raises(InvalidInputError) as excinfo:
        create_student.execute(input_create_student)
    assert excinfo.value.args[0] == "Invalid email address"
