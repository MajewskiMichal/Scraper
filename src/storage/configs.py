import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# database configuration
engine = sqlalchemy.create_engine(
    'mysql+pymysql://{username}:{password}@{host}:{port}/{schema}'.format(
        username=os.environ[''],
        password=os.environ[''],
        host=os.environ[''],
        port=os.environ[''],
        schema=os.environ[''],
    )
)
Session = sessionmaker(bind=engine)
session = Session()
metadata = sqlalchemy.MetaData(bind=engine)