from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy import select

from .schema import *

from database.psql import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from utils.exceptions import HTTPError

router = APIRouter()


@cbv(router)
class JournalRouter:

    session: AsyncSession = Depends(get_db)

    @router.get(
        path='/journal/{journal_id}/head',
        status_code=200,
        response_model=Journal,
        summary="Информация о журнале",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал не найден'
            }
        }
    )
    @router.get(
        path='/journal/{journal_id}',
        status_code=200,
        response_model=JournalReadWithStudent,
        summary="Журнал со списком студентов",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал не найден'
            }
        }
    )
    async def get_journal(self, journal_id: int):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail="invalid parameter")
        journal = await self.session.get(Journal, journal_id)
        if journal is None:
            raise HTTPException(status_code=404, detail='Journal not found')
        return journal

    @router.get(
        path='/journals',
        status_code=200,
        response_model=List[JournalRead],
        responses={
            400: {
                'model': HTTPError,
                'description': 'Невалидные Query параметры'
            }
        }
    )
    async def get_all_journals(self, offset: int = 0, limit: int = 10):
        if limit > 100 or limit < 1 or offset < 0:
            raise HTTPException(status_code=400, detail='Invalid Query params')
        res = await self.session.execute(select(Journal).offset(offset).limit(limit))
        return [x[0] for x in res.all()]

    @router.patch(
        path='/journal/{journal_id}/head',
        status_code=200,
        response_model=Journal,
        summary="Обновление информации о журнале",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал не найден'
            }
        }
    )
    async def update_journal(self, journal_id: int, new_journal: JournalUpdate):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail='Invalid id')
        db_journal = await self.session.get(Journal, journal_id)
        if db_journal is None:
            raise HTTPException(status_code=404, detail='Journal not found')

        journal_data = new_journal.dict(exclude_unset=True)
        for k, v in journal_data.items():
            setattr(db_journal, k, v)

        self.session.add(db_journal)
        await self.session.commit()
        await self.session.refresh(db_journal)
        return db_journal

    @router.delete(
        path='/journal/{journal_id}',
        status_code=200,
        response_model=None,
        summary="Удаление журнала",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал не найден'
            }
        }
    )
    async def delete_journal(self, journal_id: int):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail='Invalid id')
        db_journal = await self.session.get(Journal, journal_id)
        if db_journal is None:
            raise HTTPException(status_code=404, detail='Journal not found')
        await self.session.delete(db_journal)
        await self.session.commit()

        return None

    @router.post(
        path='/journal',
        status_code=200,
        response_model=Journal,
        summary="Создание журнала"
    )
    async def create_journal(self, journal: JournalCreate) -> Journal:
        db_journal = Journal.from_orm(journal)
        self.session.add(db_journal)
        await self.session.commit()
        await self.session.refresh(db_journal)

        return db_journal

    @router.get(
        path='/journal/{journal_id}/student/{student_id}',
        response_model=Student,
        summary="Информация о студенте",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал или студент не найден'
            }
        }
    )
    async def get_student(self, journal_id: int, student_id: int):
        if journal_id < 1 or student_id < 1:
            raise HTTPException(status_code=400, detail="Invalid ID param")
        res = await self.session.execute(
            select(Student).where(Student.journal_id == journal_id).where(Student.id == student_id)
        )
        st = res.one_or_none()
        if st is None:
            raise HTTPException(status_code=404, detail='Student not found')
        return st[0]

    @router.post(
        path='/journal/{journal_id}/students',
        status_code=200,
        response_model=List[StudentRead],
        response_model_exclude={"journal_id"},
        summary="Добавление студентов к журналу",
        responses = {
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал или студент не найден'
            }
        }
    )
    async def add_student(self, journal_id: int, students: List[StudentCreate], ):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail='Invalid ID param')

        journal = await self.session.get(Journal, journal_id)
        if journal is None:
            raise HTTPException(status_code=404, detail='Journal Not found')

        """
        TODO:
            Вопрос производительности, нужно использовать bulk_insert_mappings в sync режиме
        """
        res = []
        for student in students:
            st = Student.from_orm(student)
            st.journal_id = journal_id
            self.session.add(st)
            await self.session.commit()
            await self.session.refresh(st)
            res.append(st)
        return res

    @router.patch(
        path='/journal/{journal_id}/student/{student_id}',
        response_model=StudentRead,
        summary="Изменение стундента в журнале",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал или студент не найден'
            }
        }
    )
    async def update_student(self, journal_id: int, student_id: int, new_student: StudentUpdate):
        if journal_id < 1 or student_id < 1:
            raise HTTPException(status_code=400, detail='Invalid ID param')

        db_student = await self.get_student(journal_id, student_id)

        student_data = new_student.dict(exclude_unset=True)
        for k, v in student_data.items():
            setattr(db_student, k, v)

        self.session.add(db_student)
        await self.session.commit()
        await self.session.refresh(db_student)

        return db_student

    @router.delete(
        path='/journal/{journal_id}/student/{student_id}',
        response_model=None,
        summary="Удаление студента в журнале",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал или студент не найден'
            }
        }
    )
    async def delete_student(self, journal_id: int, student_id: int):
        if journal_id < 1 or student_id < 1:
            raise HTTPException(status_code=400, detail='Invalid ID param')

        db_st = await self.get_student(journal_id, student_id)

        await self.session.delete(db_st)
        await self.session.commit()
        return None

    @router.get(
        path='/journal/{journal_id}/table',
        response_model=List[JournalTableRead],
        summary="Таблица посещаемости",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал не найден'
            }
        }
    )
    async def get_journal_table(self, journal_id: int, date_start: datetime.date, date_end: datetime.date):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail='Invalid id')

        stmt = select([JournalTable])\
            .where(JournalTable.journal_id == journal_id)\
            .where(JournalTable.date.between(date_start, date_end))
        execute = await self.session.execute(stmt)
        result = []
        for row in execute.all():
            result.append(row[0])

        return result

    @router.post(
        path='/journal/{journal_id}/table',
        response_model=List[JournalTableRead],
        summary="Добавление записей в таблицу посещаемости (работает и на замену)",
        responses={
            400: {
                'model': HTTPError,
                'description': 'Некорректный ID или state, повторяющиеся ячейки таблицы'
            },
            404: {
                'model': HTTPError,
                'description': 'Журнал или студент не найден'
            }
        }
    )
    async def create_update_journal(self, journal_id: int, cells: List[JournalTableCreateUpdate]):
        if journal_id < 1:
            raise HTTPException(status_code=400, detail='Invalid ID')

        for c in cells:
            if c.student_id < 1:
                raise HTTPException(status_code=400, detail='Invalid ID')

        journal = await self.session.get(Journal, journal_id)
        if journal is None:
            raise HTTPException(status_code=404, detail='Journal not found')

        for c in cells:
            if c.student_id not in [x.id for x in journal.students]:
                raise HTTPException(status_code=404, detail='Student not found')
            if c.state not in (0, 1, 2):
                raise HTTPException(status_code=400, detail='Invalid state')

            if [(x.date, x.student_id) for x in cells].count((c.date, c.student_id)) > 1:
                raise HTTPException(status_code=400, detail='Duplicate table cells')

            db_cell = await self.session.get(JournalTable, (journal_id, c.student_id, c.date))
            if db_cell is None:
                if c.state == 0:
                    continue
                data = JournalTable.from_orm(c)
                data.journal_id = journal_id
                self.session.add(data)

            else:
                if c.state == 0:
                    await self.session.delete(db_cell)
                    continue

                data = c.dict(exclude_unset=True)
                for k, v in data.items():
                    setattr(db_cell, k, v)
                self.session.add(db_cell)

        await self.session.commit()
        return cells
