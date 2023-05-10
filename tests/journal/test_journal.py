from uuid import uuid4

import pytest

from journal.schema import *
from fastapi.testclient import TestClient

"""Fixtures"""
from tests.client import test_client # noqa


@pytest.fixture()
def basic_journals() -> List[JournalCreate]:
    return [
        JournalCreate(groupName=uuid4().__str__()),
        JournalCreate(groupName=uuid4().__str__()),
        JournalCreate(groupName=uuid4().__str__())
    ]


@pytest.fixture()
def test_journal_create(test_client: TestClient, basic_journals: List[JournalCreate]):
    _id = 1
    for journal in basic_journals:
        response = test_client.post('/journal', json=journal.dict())
        assert response.status_code == 200

        response_data = Journal(**response.json())
        assert response_data.id == _id
        assert response_data.groupName == journal.groupName

        _id += 1

    yield basic_journals

    for journal_id in range(1, 4):
        response = test_client.delete(f'/journal/{journal_id}')
        assert response.status_code == 200


@pytest.fixture()
def test_testing_journals_with_students(test_client: TestClient):
    """
    Создаёт журнал (id = 1, 2)
    и добавляет 3 студента в каждый (id = 1, 2, 3, 4, 5, 6)
    """
    resp = test_client.post('/journal', json=JournalCreate(groupName='1').dict())
    assert resp.status_code == 200
    assert resp.json().get('id') == 1

    resp = test_client.post('/journal', json=JournalCreate(groupName='2').dict())
    assert resp.status_code == 200
    assert resp.json().get('id') == 2

    resp = test_client.post('/journal/1/students', json=[
        StudentCreate(fullName='1').dict(),
        StudentCreate(fullName='2').dict(),
        StudentCreate(fullName='3').dict()
    ])
    assert resp.status_code == 200
    for st in resp.json():
        assert StudentRead(**st).id in (1, 2, 3)

    resp = test_client.get('/journal/1/student/1')
    assert resp.status_code == 200

    resp = test_client.post('/journal/2/students', json=[
        StudentCreate(fullName='4').dict(),
        StudentCreate(fullName='5').dict(),
        StudentCreate(fullName='6').dict()
    ])
    assert resp.status_code == 200

    yield

    """ Teardown Удаление журналов """
    resp = test_client.delete('/journal/1')
    assert resp.status_code == 200
    resp = test_client.delete('/journal/2')
    assert resp.status_code == 200

    """ Проверка каскадного удаления студентов """
    resp = test_client.get('/journal/1/student/1')
    assert resp.status_code == 404


def test_get_all_journals(test_client, test_journal_create):
    resp = test_client.get('/journals')
    assert resp.status_code == 200
    stored_journals = [JournalRead(**x) for x in resp.json()]
    assert len(stored_journals) == 3

    for x in stored_journals:
        assert x.id in (1, 2, 3)
        assert x.groupName in [x.groupName for x in test_journal_create]


def test_get_all_journals_limit(test_client, test_journal_create):
    resp = test_client.get('/journals', params={'limit': 1})
    assert resp.status_code == 200
    stored_journals = [JournalRead(**x) for x in resp.json()]
    assert len(stored_journals) == 1

    for x in stored_journals:
        assert x.id in (1, 2, 3)
        assert x.groupName in [x.groupName for x in test_journal_create]


def test_journal_update(test_client: TestClient, test_journal_create):
    journal_id = 2
    data = JournalUpdate(
        groupName=uuid4().__str__()
    )

    response = test_client.patch(f'/journal/{journal_id}/head', json=data.dict())
    assert response.status_code == 200
    response_data = Journal(**response.json())

    assert response_data.groupName == data.groupName

    response = test_client.get(f'/journal/{journal_id}/head')
    assert response.status_code == 200
    response_data = Journal(**response.json())

    assert response_data.groupName == data.groupName


class TestStudents:

    @pytest.fixture(scope='class')
    def test_journals(self, test_client):
        ids = []
        for journal in [JournalCreate(groupName=uuid4().__str__()) for _ in range(2)]:
            response = test_client.post('/journal', json=journal.dict())
            assert response.status_code == 200
            response_data = Journal(**response.json())
            ids.append(response_data.id)

        yield ids[0]

        for i in ids:
            response = test_client.delete(f'/journal/{i}')
            assert response.status_code == 200

    @pytest.fixture(scope='class')
    def test_students_data(self) -> List[StudentCreate]:
        return [
            StudentCreate(fullName=uuid4().__str__()) for _ in range(25)
        ]

    @pytest.fixture()
    def test_add_students(self, test_client, test_students_data, test_journals):
        journal_id = test_journals
        response = test_client.post(f'/journal/{journal_id}/students', json=[x.dict() for x in test_students_data])
        assert response.status_code == 200

        student_id = 1
        inserted_students = []
        for response_item in response.json():
            data = Student(**response_item)

            assert (data.fullName in [x.fullName for x in test_students_data])
            assert data.id == student_id
            student_id += 1
            inserted_students.append(data)

        yield inserted_students

        for i in inserted_students:
            response = test_client.delete(f'/journal/{journal_id}/student/{i.id}')
            assert response.status_code == 200

    def test_update_students(self, test_client, test_journals, test_add_students):
        journal_id = test_journals
        new_students = [StudentUpdate(fullName=uuid4().__str__()) for _ in test_add_students]

        for i in range(len(test_add_students)):
            response = test_client.patch(f'/journal/{journal_id}/student/{test_add_students[i].id}',
                                         json=new_students[i].dict())
            assert response.status_code == 200

            response_data = StudentRead(**response.json())
            assert response_data.id == test_add_students[i].id
            assert response_data.fullName == new_students[i].fullName
