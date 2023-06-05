import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    response = client.get(f'/api/v1/courses/{course_id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name

@pytest.mark.django_db
def test_list_course(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == course
    for i, m in enumerate(data):
        assert m['name'] == course[i].name

@pytest.mark.django_db
def test_filter_id_course(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/', data={'id': course[0].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course[0].id

@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/', data={'name': course[0].name})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course[0].name

@pytest.mark.django_db
def test_post_course(client):
    stedent_1 = Student.objects.create(name='s1', birth_date='05/02/2001')
    stedent_2 = Student.objects.create(name='s2', birth_date='05/02/2002')
    response = client.post('/api/v1/courses/', data={
        'name': 'course_1',
        'students': [stedent_1.id, stedent_2.id]
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_patch_course(client, course_factory):
    student = Student.objects.create(name='student_1', birth_date='1993-01-10')
    course = course_factory(_quantity=1)
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={
        'students': [student.id]
    })
    assert response.status_code == 200
    data = response.json()
    assert data['students'] == [student.id]


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=2)
    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204




