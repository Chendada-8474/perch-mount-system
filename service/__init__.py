import sqlalchemy
import sqlalchemy.orm

from src import config

DATABASE_NAME = "perch_mount"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (
    config.get_env(config.EnvKeys.MYSQL_USER),
    config.get_env(config.EnvKeys.MYSQL_PASSWORD),
    config.get_env(config.EnvKeys.MYSQL_HOST),
    config.get_env(config.EnvKeys.MYSQL_PORT),
    DATABASE_NAME,
)

db_engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=3600,
    pool_pre_ping=True,
    # isolation_level="AUTOCOMMIT",
)


session = sqlalchemy.orm.sessionmaker(db_engine, expire_on_commit=False)
