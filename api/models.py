import os
import sqlalchemy as sa
from dotenv import load_dotenv
load_dotenv()


def connect():
    user = os.environ.get("DB_USER")
    db_name = os.environ.get("DB_NAME")
    db_pass = os.environ.get("DB_PASS")
    db_port = os.environ.get("DB_PORT")
    db_host = os.environ.get("DB_HOST")
    #  print(user, db_name, db_pass)
    #  print(user, db_pass, db_host, db_port, db_name)
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(user, db_pass, db_host, db_port, db_name)
    # The return value of create_engine() is our connection object
    connection = sa.create_engine(url, client_encoding="utf8")
    # We then bind the connection to MetaData()
    metadata = sa.MetaData(bind=connection)

    return connection, metadata


con, meta = connect()
