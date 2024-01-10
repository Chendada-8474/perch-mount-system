from src.config import MySQL as ConfMySQL
from sqlalchemy import create_engine

DATABASE_NAME = "perch_mount"


db_engine = create_engine(
    "mysql+pymysql://%s:%s@%s:%s/%s"
    % (
        ConfMySQL.get_mysql_user(),
        ConfMySQL.get_mysql_password(),
        ConfMySQL.get_mysql_host(),
        ConfMySQL.get_mysql_port(),
        DATABASE_NAME,
    ),
    pool_recycle=3600,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
)
