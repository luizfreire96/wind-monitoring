import os
import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:

    db_host = os.environ["instance-host"]
    db_user = os.environ["db-user"]
    db_pass = os.environ["db-pass"]
    db_name = os.environ["db-name"]
    db_port = os.environ["db-port"]

    pool = sqlalchemy.create_engine(

        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+psycopg2",
            username=db_user,
            password=db_pass,
            host=db_host,
            database=db_name,
            port=db_port,
        ),
        # ...
    )
    return pool
