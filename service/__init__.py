import sqlalchemy
import sqlalchemy.orm

from src import config

DATABASE_NAME = "perch_mount"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (
    config.MySQL.get_mysql_user(),
    config.MySQL.get_mysql_password(),
    config.MySQL.get_mysql_host(),
    config.MySQL.get_mysql_port(),
    DATABASE_NAME,
)

db_engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=3600,
    pool_pre_ping=True,
    # isolation_level="AUTOCOMMIT",
)


session = sqlalchemy.orm.sessionmaker(db_engine)
