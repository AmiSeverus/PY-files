import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()

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
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)

    response = client.get(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 200
    data = response.json()
    assert courses[0].name == data['name']

@pytest.mark.django_db
def test_get_courses(client, course_factory):
    course_factory(_quantity=5, make_m2m=True)
    count = Course.objects.count()

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == count

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name':'test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)[0]

    response = client.patch(f'/api/v1/courses/{course.id}/', data={'name':'test'})

    assert response.status_code == 200

    assert Course.objects.get(pk=course.id).name == 'test'

@pytest.mark.django_db
def test_course_filter_by_id(client, course_factory):
    course = course_factory(_quantity=10)[0]

    response = client.get(f'/api/v1/courses/?id = {course.id}/')

    assert response.status_code == 200

    assert Course.objects.filter(id=course.id).count() == 1

@pytest.mark.django_db
def test_course_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    test_course = courses[0]
    count = 0
    for course in courses:
        if course.name == test_course.name:
            count += 1

    response = client.get(f'/api/v1/courses/?id = {test_course.id}/')

    assert response.status_code == 200

    assert Course.objects.filter(name=test_course.name).count() == count

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)[0]

    response = client.delete(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 204

    assert Course.objects.filter(id=course.id).count() == 0

# @pytest.mark.django_db
# def test_example():
#     assert False, "Just test example"