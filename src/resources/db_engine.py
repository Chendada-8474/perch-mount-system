import sys
from os.path import dirname
from sqlalchemy import create_engine

sys.path.append(dirname(dirname(__file__)))
import configs.mysql


master_engine = create_engine(
    "mysql+pymysql://%s:%s@%s:%s/%s"
    % (
        configs.mysql.master_user,
        configs.mysql.master_passward,
        configs.mysql.master_ip,
        configs.mysql.master_port,
        configs.mysql.database,
    ),
    pool_recycle=3600,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
)

slave_engine = create_engine(
    "mysql+pymysql://%s:%s@%s:%s/%s"
    % (
        configs.mysql.slave_user,
        configs.mysql.slave_passward,
        configs.mysql.slave_ip,
        configs.mysql.slave_port,
        configs.mysql.database,
    ),
    pool_recycle=3600,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
)
