from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


def create_database():
    # creating database engine
    engine = create_engine('sqlite:////tmp/mario.db')

    # creating session to work with database
    db_session = scoped_session(sessionmaker(bind=engine))
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
    table = Entries
    base.metadata.create_all(engine, tables=[table.__table__])

    return table


def add_entry(session, table, entry):
    # add entry and commit it to database
    session.add(table(**entry))
    session.commit()


def convert_rows_to_dict(query):
    result = []
    for row in query:
        row_dict = row.__dict__
        row_dict.pop('_sa_instance_state')  # deleting orm object
        result.append(row_dict)

    return result


def select_all_from(session, table):
    """
    Function to select all from provided table (like SELECT * FROM table)
    :param session: sqlalchemy session
    :param table: table to select from
    :return: list of rows in table as dictionaries
    """
    # querying stuff from db
    query = session.query(table).all()
    return convert_rows_to_dict(query)


def select_id_from(session, table, id):
    """
    Function to select specific id from provided table (like SELECT * FROM table WHERE table.id=id)
    :param session: sqlalchemy session
    :param table: table to select from
    :param id: id to get
    :return: list of rows in table as dictionaries
    """
    # querying stuff from db
    query = session.query(table).filter(table.id == id)
    return convert_rows_to_dict(query)


def select_count_from(session, table):
    count = session.query(table).count()
    return count
