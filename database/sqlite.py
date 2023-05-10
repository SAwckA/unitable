# from sqlmodel import SQLModel, create_engine, Session
#
#
# engine = create_engine('sqlite+pysqlite:///./debug.db', echo=True, future=True, connect_args={"check_same_thread": False})
#
# from journal import model # noqa
#
# SQLModel.metadata.create_all(engine)
#
#
# def get_db() -> Session:
#     with Session(engine) as session:
#         yield session
