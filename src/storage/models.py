from sqlalchemy import *
from .configs import metadata

# tables from db

parse_request = Table('parse_request', metadata,
           Column('id', Integer),
           Column('url', String),
           Column('type', String),
           Column('status', String)
          )

parse_result_text = Table('parse_result_text', metadata,
           Column('id', Integer),
           Column('parse_request_id', String), #fk
           Column('content', String)
          )

parse_result_image = Table('parse_result_image', metadata,
          Column('id', Integer),
          Column('parse_request_id', Integer), #fk
          Column('filename', String)
          )