import datetime

from pydantic import BaseModel, validator, ValidationError
from sqlmodel import SQLModel, Relationship, Field, UniqueConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from pydantic.fields import Field as PField
from sqlalchemy.orm import relationship

from typing import Optional, List


class JournalBase(SQLModel):
    groupName: str


class Journal(JournalBase, table=True):
    __tablename__ = 'journal'
    id: Optional[int] = Field(default=None, primary_key=True)

    students: List["Student"] = Relationship(back_populates='journal',
                                             sa_relationship_kwargs={'lazy': 'selectin', 'cascade': 'delete'})


class JournalCreate(JournalBase):
    pass


class JournalRead(JournalBase):
    id: int


class JournalUpdate(JournalBase):
    groupName: str


class StudentBase(SQLModel):
    fullName: str


class Student(StudentBase, table=True):
    __tablename__ = 'student'
    # __table_args__ = (ForeignKeyConstraint(('journal_id',), ('journal.id',), 'journal_id_constraint'),)
    __table_args = (PrimaryKeyConstraint('id', 'journal_id'))
    id: Optional[int] = Field(default=None, primary_key=True)
    journal: Optional[Journal] = Relationship(back_populates='students', sa_relationship_kwargs={'lazy': 'selectin'})

    journal_id: int = Field(default=None, foreign_key='journal.id')


class StudentRead(StudentBase):
    id: int


class StudentCreate(StudentBase): ...


class StudentUpdate(StudentBase):
    fullName: str


class JournalReadWithStudent(JournalRead):
    students: List[StudentRead] = []


class StudentReadWithJournal(JournalRead):
    journal: Optional[JournalRead] = None


class JournalTableBase(SQLModel):
    date: datetime.date
    student_id: int
    state: int


class JournalTable(JournalTableBase, table=True):
    __tablename__ = 'journal_table'
    __table_args__ = (
        UniqueConstraint("journal_id", "date", "student_id"),
        PrimaryKeyConstraint('journal_id', 'student_id', 'date')
    )

    journal_id: Optional[int] = Field(default=None, foreign_key='journal.id')
    date: datetime.date = Field(default=None, nullable=False)
    student_id: int = Field(default=None, foreign_key='student.id')
    state: int = Field(default=0, nullable=False)


class JournalTableRead(JournalTableBase):
    ...


class JournalTableCreateUpdate(JournalTableBase):
    ...



#
# class Student(BaseModel):
#     id: int
#     firstName: str
#     lastName: str
#     middleName: str | None
#
#
# class CreateStudent(BaseModel):
#     firstName: str
#     lastName: str
#     middleName: str | None
#
#
# class UpdateStudent(CreateStudent): ...
#
#
# class JournalHead(BaseModel):
#     id: int
#     groupName: str
#     students: list[Student]
#
#
# class CreateJournal(BaseModel):
#     groupName: str
#     students: list[CreateStudent]
#
#
# class UpdateJournalHead(CreateJournal): ...
#
#
# class JournalCell(BaseModel):
#     student_id: int
#     state: int
#     date: datetime.date
#
#     @validator('state')
#     def validate_state(cls, v: int):
#         if 1 <= v <= 3:
#             return v
#         raise ValidationError('Invalid state')
#
#
# class JournalTable(BaseModel):
#     journalTable: list[JournalCell]
#
#
# class UpdateCell(BaseModel):
#     student_id: int
#     state: int
#     date: datetime.date
#
