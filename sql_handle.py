from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float


def create_database():
    """
    Function to initialize DB
    :return: engine, session, base
    """
    # creating database engine
    engine = create_engine(r'sqlite:///D:\sqlite\dbmario.db', connect_args={'check_same_thread': False})

    # creating session to work with database
    db_session = scoped_session(sessionmaker(bind=engine))
    session = db_session()

    # creating base for declarations
    base = declarative_base()

    return engine, session, base


def create_entries_table(engine, base):
    """
    Function to describe entries table and create it in the DB
    :param engine: sqlalchemy engine
    :param base: sqlalchemy base
    :return: described table
    """
    # describing table for entries
    class Entries(base):
        __tablename__ = 'entries'

        id = Column(Integer, primary_key=True)
        grid_size = Column(Integer)
        grid = Column(String)
        error_flag = Column(Boolean)
        path = Column(String)
        request_time = Column(Float)

        def __repr__(self):
            return 'Grid size {}, Grid {}, Error_flag: {}, Path {}'.format(self.grid_size, self.grid, self.error_flag,
                                                                           self.path)

    # actually creating described table
    table = Entries
    if not engine.dialect.has_table(engine, 'entries'):
        base.metadata.create_all(engine, tables=[table.__table__])
    # if described table exists, drop it to truncate
    else:
        table.__table__.drop(engine)
        base.metadata.create_all(engine, tables=[table.__table__])

    return table


def add_entry(session, table, entry):
    """
    Add entry and commit it to database (like INSERT INTO, COMMIT)
    :param session: sqlalchemy session
    :param table: table to select from
    :param entry: dictionary with row
    """
    session.add(table(**entry))
    session.commit()


def convert_rows_to_dict(query) -> list:
    """
    Function to convert query rows to readable dictionary
    :param query: sqlalchemy query
    :return:
    """
    result = []
    for row in query:
        row_dict = row.__dict__
        row_dict.pop('_sa_instance_state')  # deleting orm object
        result.append(row_dict)

    return result


def select_all_from(session, table) -> list:
    """
    Function to select all from provided table (like SELECT * FROM table)
    :param session: sqlalchemy session
    :param table: table to select from
    :return: list of rows in table as dictionaries
    """
    # querying all stuff from db
    query = session.query(table).all()
    return convert_rows_to_dict(query)


def select_id_from(session, table, id) -> list:
    """
    Function to select specific id from provided table (like SELECT * FROM table WHERE table.id=id)
    :param session: sqlalchemy session
    :param table: table to select from
    :param id: id to get
    :return: list of rows in table as dictionaries
    """
    # querying specific stuff from db
    query = session.query(table).filter(table.id == id)
    return convert_rows_to_dict(query)


def select_count_from(session, table) -> int:
    """
    Function to select row count from provided table (like SELECT COUNT(*) FROM table)
    :param session: sqlalchemy session
    :param table: table to select from
    :return: row count
    """
    count = session.query(table).count()
    return count
