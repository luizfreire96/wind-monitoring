import os
import sqlalchemy

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    db_host = os.environ["instance-host"]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = os.environ["db-user"]  # e.g. 'my-db-user'
    db_pass = os.environ["db-pass"]  # e.g. 'my-db-password'
    db_name = os.environ["db-name"]  # e.g. 'my-database'
    db_port = os.environ["db-port"]  # e.g. 3306

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/
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