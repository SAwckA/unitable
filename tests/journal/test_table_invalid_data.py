import json
import logging
from typing import List
from datetime import date

import pytest
from fastapi.testclient import TestClient
from journal.schema import *

from tests.client import test_client
from tests.journal.test_journal import (
    test_journal_create,
    basic_journals,
    test_testing_journals_with_students
)


def test_get_table_invalid_journal_id(test_client: TestClient, test_testing_journals_with_students):
    resp = test_client.get('/journal/-1/table', params={
        'date_start': datetime.date(2010, 1, 2).strftime('%Y-%m-%d'),
        'date_end': datetime.date(2010, 2, 5).strftime('%Y-%m-%d')}
                           )
    assert resp.status_code == 400


def test_create_table_invalid_journal_id(test_client: TestClient):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
    ]
    resp = test_client.post('/journal/-1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 400


def test_create_table_invalid_student_id(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=-1, state=1),
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 400


def test_create_table_not_exists_journal(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=1)
    ]
    resp = test_client.post('/journal/999/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 404


def test_create_table_not_exists_students(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=999, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=999, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=999, state=1)
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 404


def test_create_table_duplicate_keys(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 400


def test_create_table_duplicate_state(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=2),
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 400


def test_create_table_invalid_state(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=100),
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=12),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=1)
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 400


def test_create_table_not_same_journal_student(test_client, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=4, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=5, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=6, state=1)
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 404


def test_delete_journal_with_table(test_client: TestClient):
    resp = test_client.post('/journal', json=JournalCreate(groupName='1').dict())
    resp = test_client.post('/journal/1/students', json=[
        StudentCreate(fullName='1').dict(),
        StudentCreate(fullName='2').dict(),
        StudentCreate(fullName='3').dict()
    ])
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=1)
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    resp = test_client.delete('/journal/1')
    assert resp.status_code == 200

    resp = test_client.get('/journal/1')
    assert resp.status_code == 404

