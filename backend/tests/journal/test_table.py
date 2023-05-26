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


def test_create_table(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=2),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=2, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=3, state=2),
        JournalTableCreateUpdate(date=date(2023, 2, 3), student_id=3, state=1),
        JournalTableCreateUpdate(date=date(2023, 12, 3), student_id=2, state=1),
        JournalTableCreateUpdate(date=date(2023, 11, 3), student_id=3, state=2),
        JournalTableCreateUpdate(date=date(2023, 11, 3), student_id=2, state=1),

    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    for i in range(len(data)):
        assert JournalTableRead(**resp.json()[i]).date == data[i].date
        assert JournalTableRead(**resp.json()[i]).student_id == data[i].student_id
        assert JournalTableRead(**resp.json()[i]).state == data[i].state


    """ Teardown """
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=2, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=3, state=0),
        JournalTableCreateUpdate(date=date(2023, 2, 3), student_id=3, state=0),
        JournalTableCreateUpdate(date=date(2023, 12, 3), student_id=2, state=0),
        JournalTableCreateUpdate(date=date(2023, 11, 3), student_id=3, state=0),
        JournalTableCreateUpdate(date=date(2023, 11, 3), student_id=2, state=0),
    ]
    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200



def test_create_table_override(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=1),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=2),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=1),
    ]

    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    for i in range(len(data)):
        assert JournalTableRead(**resp.json()[i]).date == data[i].date
        assert JournalTableRead(**resp.json()[i]).student_id == data[i].student_id
        assert JournalTableRead(**resp.json()[i]).state == data[i].state

    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=1, state=2),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=1, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=1, state=2),
    ]

    resp = test_client.post('/journal/1/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    resp = test_client.get('/journal/1/table', params={
        'date_start': datetime.date(2000, 1, 1).strftime('%Y-%m-%d'),
        'date_end': datetime.date(3000, 1, 1).strftime('%Y-%m-%d')})
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    assert JournalTableRead(**resp.json()[0]).date == data[0].date
    assert JournalTableRead(**resp.json()[0]).student_id == data[0].student_id
    assert JournalTableRead(**resp.json()[0]).state == data[0].state

    assert JournalTableRead(**resp.json()[1]).date == data[2].date
    assert JournalTableRead(**resp.json()[1]).student_id == data[2].student_id
    assert JournalTableRead(**resp.json()[1]).state == data[2].state


def test_create_table_nulls(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2023, 1, 1), student_id=4, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 2), student_id=5, state=0),
        JournalTableCreateUpdate(date=date(2023, 1, 3), student_id=6, state=0),
    ]

    resp = test_client.post('/journal/2/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    resp = test_client.get('/journal/2/table', params={
        'date_start': datetime.date(2000, 1, 1).strftime('%Y-%m-%d'),
        'date_end': datetime.date(3000, 1, 1).strftime('%Y-%m-%d')}
                           )
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_get_table_date_filter(test_client: TestClient, test_testing_journals_with_students):
    data: List[JournalTableCreateUpdate] = [
        JournalTableCreateUpdate(date=date(2010, 1, 1), student_id=4, state=1),
        JournalTableCreateUpdate(date=date(2010, 1, 2), student_id=5, state=1),
        JournalTableCreateUpdate(date=date(2010, 2, 3), student_id=6, state=1),
        JournalTableCreateUpdate(date=date(2010, 2, 4), student_id=6, state=1),
        JournalTableCreateUpdate(date=date(2010, 2, 5), student_id=6, state=1),
        JournalTableCreateUpdate(date=date(2010, 2, 6), student_id=6, state=1),
    ]

    resp = test_client.post('/journal/2/table', content=json.dumps([x.dict() for x in data], default=str, indent=4))
    logging.info(resp.json())
    assert resp.status_code == 200

    resp = test_client.get('/journal/2/table', params={
        'date_start': datetime.date(2010, 1, 2).strftime('%Y-%m-%d'),
        'date_end': datetime.date(2010, 2, 5).strftime('%Y-%m-%d')}
                           )
    assert resp.status_code == 200
    assert len(resp.json()) == 4
