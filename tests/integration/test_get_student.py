from src.application.usecases.get_student import GetStudent
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.application.errors.application_erros import StudentNotFoundError
import pytest

student_dao = StudentDaoMemory()

def test_get_student_should_return_student_properly():
    get_student = GetStudent(student_dao)
    student = get_student.execute("ENR557596")
    assert student.name == "Anthony Smith"
    assert student.age == 27
    assert student.major == "Logistics"
    assert student.email == "anthonysmith@harvard.com"
    assert student.id is not None
    assert student.enrollment_id == "ENR557596"

def test_get_student_should_throw_exception_for_nonexistent_student():
    get_student = GetStudent(student_dao)
    with pytest.raises(StudentNotFoundError) as excinfo:
        get_student.execute("ENR999999")
    assert excinfo.value.args[0] == "Student with enrollment id ENR999999 not found"