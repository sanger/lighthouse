from typing import Any, Dict, List, Optional
from flask import current_app as app

import sqlalchemy # type: ignore
from sqlalchemy.engine.base import Engine # type: ignore
from sqlalchemy import MetaData # type: ignore

def create_mlwh_connection_engine(connection_string: str, database: str) -> Engine:
  create_engine_string = f"mysql+pymysql://{connection_string}/{database}"
  return sqlalchemy.create_engine(create_engine_string, pool_recycle=3600)

def get_table(sql_engine: Engine, table_name: str):
  metadata = MetaData(sql_engine)
  metadata.reflect()
  return metadata.tables[table_name]
