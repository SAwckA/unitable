import pytest

from journal.schema import *
from fastapi.testclient import TestClient

"""Fixtures"""
from tests.client import test_client # noqa
from tests.journal.test_journal import (
    test_journal_create,
    basic_journals,
    test_testing_journals_with_students
)

import logging


class TestJournalInvalidData:
    @staticmethod
    def test_get_journal_not_found(test_client: TestClient):
        resp = test_client.get('/journal/1')
        assert resp.status_code == 404

    @staticmethod
    def test_get_journal_invalid_id(test_client: TestClient):
        resp = test_client.get('/journal/-1')
        assert resp.status_code == 400

    @staticmethod
    def test_update_journal_not_found(test_client: TestClient):
        resp = test_client.patch('/journal/1/head', json=JournalUpdate(groupName='123').dict())
        assert resp.status_code == 404

    @staticmethod
    def test_update_journal_invalid_id(test_client: TestClient):
        resp = test_client.patch('/journal/-1/head', json=JournalUpdate(groupName='123').dict())
        assert resp.status_code == 400

    @staticmethod
    def test_delete_journal_not_found(test_client: TestClient):
        resp = test_client.delete('/journal/1')
        assert resp.status_code == 404

    @staticmethod
    def test_delete_journal_invalid_id(test_client: TestClient):
        resp = test_client.delete('/journal/-1')
        assert resp.status_code == 400

    @staticmethod
    def test_get_all_journals_invalid_limit(test_client):
        resp = test_client.get('/journals', params={'limit': 101})
        assert resp.status_code == 400
        resp = test_client.get('/journals', params={'limit': 0})
        assert resp.status_code == 400

    @staticmethod
    def test_get_all_journals_invalid_offset(test_client):
        resp = test_client.get('/journals', params={'offset': -1})
        assert resp.status_code == 400


class TestStudentInvalidData:
    @staticmethod
    def test_get_student_invalid_id(test_client, test_journal_create):
        resp = test_client.get('/journal/1/student/-1')
        assert resp.status_code == 400

        resp = test_client.get('/journal/-1/student/1')
        assert resp.status_code == 400

    @staticmethod
    def test_get_student(test_client: TestClient, test_journal_create):
        resp = test_client.get('/journal/1/student/1')
        logging.log(logging.INFO, str(resp.json()))
        assert resp.status_code == 404

    @staticmethod
    def test_create_student_invalid_id(test_client: TestClient, test_journal_create):
        resp = test_client.post('/journal/-1/students', json=[StudentCreate(fullName='123').dict(), ])
        logging.info(resp.json())
        assert resp.status_code == 400

    @staticmethod
    def test_create_student_not_found_journal(test_client: TestClient):
        resp = test_client.post('/journal/999/students', json=[StudentCreate(fullName='123').dict(), ])
        logging.info(resp.json())
        assert resp.status_code == 404

    @staticmethod
    def test_update_student_invalid_id(test_client: TestClient, test_journal_create):
        resp = test_client.patch('/journal/1/student/-1', json=StudentUpdate(fullName='123').dict())
        assert resp.status_code == 400

    @staticmethod
    def test_update_student_invalid_journal_id(test_client: TestClient, test_journal_create):
        resp = test_client.patch('/journal/-1/student/1', json=StudentUpdate(fullName='123').dict())
        assert resp.status_code == 400

    @staticmethod
    def test_update_student_not_found_journal(test_client: TestClient):
        resp = test_client.patch('/journal/1/student/1', json=StudentUpdate(fullName='123').dict())
        assert resp.status_code == 404

    @staticmethod
    def test_update_student_not_found(test_client: TestClient, test_journal_create):
        resp = test_client.patch('/journal/1/student/1', json=StudentUpdate(fullName='123').dict())
        logging.info(resp.json())
        assert resp.status_code == 404

    @staticmethod
    def test_delete_student_not_found_journal(test_client: TestClient):
        resp = test_client.delete('/journal/9999/student/1')
        assert resp.status_code == 404

    @staticmethod
    def test_delete_student_not_found(test_client: TestClient, test_journal_create):
        resp = test_client.delete('/journal/1/student/1')
        assert resp.status_code == 404

    @staticmethod
    def test_delete_student_invalid_journal_id(test_client: TestClient):
        resp = test_client.delete('/journal/-1/student/1')
        assert resp.status_code == 400

    @staticmethod
    def test_delete_student_invalid_id(test_client: TestClient):
        resp = test_client.delete('/journal/1/student/-1')
        assert resp.status_code == 400

    @staticmethod
    def test_not_same_journal_student_get(test_client, test_testing_journals_with_students):
        resp = test_client.get('/journal/1/student/4')
        assert resp.status_code == 404

    @staticmethod
    def test_not_same_journal_student_update(test_client, test_testing_journals_with_students):
        resp = test_client.patch('/journal/1/student/4', json=StudentUpdate(fullName='new name').dict())
        assert resp.status_code == 404

    @staticmethod
    def test_not_same_journal_student_delete(test_client, test_testing_journals_with_students):
        resp = test_client.delete('/journal/1/student/4')
        assert resp.status_code == 404
