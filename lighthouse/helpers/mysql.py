from typing import Optional

import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Table


def create_mysql_connection_engine(connection_string: str, database: Optional[str] = None) -> Engine:
    """Create a connection engine to the MySQL server using SQLAlchemy.

    Args:
        connection_string (str): connection string defining host, port, username and password.
        database (str, optional): database to connect to. Defaults to None.

    Returns:
        Engine: a SQLAlchemy engine
    """
    create_engine_string = f"mysql+pymysql://{connection_string}"

    if database:
        create_engine_string += f"/{database}"

    return sqlalchemy.create_engine(create_engine_string, pool_recycle=3600)


def get_table(sql_engine: Engine, table_name: str) -> Table:
    """Get a Table object from SQLAlchemy given the table name.

    Args:
        sql_engine (Engine): the engine to use.
        table_name (str): the name of the table to get.

    Returns:
        Table: a SQLAlchemy Table object.
    """
    metadata = MetaData(sql_engine)

    metadata.reflect()

    return metadata.tables[table_name]
