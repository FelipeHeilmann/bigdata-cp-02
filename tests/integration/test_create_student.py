from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.application.usecases.create_student import CreateStudent, Input
from src.application.usecases.get_student import GetStudent

student_dao = StudentDaoMemory()

def test_create_student_should_create_student_properly():
    create_student = CreateStudent(student_dao)
    input_create_student = Input(
        name="John Doe",
        enrollment_id="ENR551026",
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    ouput_create_student = create_student.execute(input_create_student)
    get_student = GetStudent(student_dao)
    output_get_student = get_student.execute(ouput_create_student.enrollment_id)
    assert output_get_student.name == "John Doe"
    assert output_get_student.age == 20
    assert output_get_student.major == "Computer Science"
    assert output_get_student.email == "johndoe@harvard.com"
    assert output_get_student.id is not None
    assert output_get_student.enrollment_id  == "ENR551026"
