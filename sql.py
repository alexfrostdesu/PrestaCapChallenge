from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


def create_database():
    # creating database engine
    engine = create_engine('sqlite:///:memory:', echo=True)

    # creating session to work with database
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # creating base for declarations
    base = declarative_base()

    return engine, session, base


def create_entries_table(engine, base):
    # describing table for entries
    class Entries(base):
        __tablename__ = 'entries'

        id = Column(Integer, primary_key=True)
        grid_size = Column(Integer)
        grid = Column(String)
        error_flag = Column(Boolean)
        path = Column(String)

        def __repr__(self):
            return 'Grid size {}, Grid {}, Error_flag: {}, Path {}'.format(self.grid_size, self.grid, self.error_flag,
                                                                           self.path)

    # actually creating described table
    base.metadata.create_all(engine, tables=[Entries.__table__])

    return Entries


def add_entry(session, table, entry):
    # add entry and commit it to database
    session.add(table(**entry))
    session.commit()


def select_all_from(session, table):
    # querying stuff from db
    query = session.query(table).all()
    for row in query:
        print(row.__dict__)

    return [row.__dict__ for row in query]
