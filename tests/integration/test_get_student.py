from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.application.usecases.create_student import CreateStudent, Input
from src.application.usecases.get_student import GetStudent
from src.application.errors.application_erros import (
    StudentNotFoundError
)
import pytest

student_dao = StudentDaoMongo()

def test_get_student_should_return_student_properly():
    create_student = CreateStudent(student_dao)
    input_create_student = Input(
        name="Anthony Smith",
        enrollment_id="ENR557596",
        age=27,
        major="Logistics",
        email="anthonysmith@harvard.com"
    )
    output_create_student = create_student.execute(input_create_student)
    get_student = GetStudent(student_dao)
    student = get_student.execute("ENR557596")
    assert student.name == "Anthony Smith"
    assert student.age == 27
    assert student.major == "Logistics"
    assert student.email == "anthonysmith@harvard.com"
    assert student.id is not None
    assert student.enrollment_id == "ENR557596"
    student_dao.remove(output_create_student.id)


def test_get_student_should_throw_exception_for_nonexistent_student():
    get_student = GetStudent(student_dao)
    with pytest.raises(StudentNotFoundError) as excinfo:
        get_student.execute("ENR999999")
    assert excinfo.value.args[0] == "Student with enrollment id ENR999999 not found"