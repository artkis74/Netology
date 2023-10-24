import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory_s(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory_s


@pytest.mark.django_db
def test_get_course_retrieve(client, course_factory):
    courses = course_factory(_quantity=10, make_m2m=True, _fill_optional=True)

    for course in courses:
        url = reverse('courses-detail', kwargs={'pk': course.id})
        response = client.get(url)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == course.name


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10, make_m2m=True)

    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, x in enumerate(data):
        assert courses[i].name == x['name']


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10, make_m2m=True)

    for course in courses:
        url = reverse('courses-list')
        response = client.get(url, data={'id': course.id})
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        data = data[0]
        assert data['name'] == course.name
        assert data['id'] == course.id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10, make_m2m=True)

    for course in courses:
        url = reverse('courses-list')
        response = client.get(url, data={'name': course.name})
        data = response.json()

        assert response.status_code == 200

        for x in data:
            assert x['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    url = reverse('courses-list')
    response = client.post(url, data={'name': 'test_course'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10, make_m2m=True, _fill_optional=True)
    students = student_factory(_quantity=10)

    for i, course in enumerate(courses):
        url = reverse('courses-detail', kwargs={'pk': course.id})
        response = client.patch(url, data={'name': 'new_test_name', 'students': students[i].id})

        assert response.status_code == 200
        assert Course.objects.get(pk=course.id).name == 'new_test_name'
        assert Course.objects.filter(students__id=students[i].id).exists()


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10, make_m2m=True, _fill_optional=True)

    for course in courses:
        url = reverse('courses-detail', kwargs={'pk': course.id})
        response = client.delete(url)

        assert response.status_code == 204
        assert Course.objects.filter(pk=course.id).exists() == False