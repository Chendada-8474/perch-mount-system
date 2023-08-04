import sys
from os.path import dirname
from sqlalchemy import create_engine

sys.path.append(dirname(dirname(__file__)))
import configs.mysql


engine = create_engine(
    "mysql+pymysql://root:%s@%s/%s"
    % (
        configs.mysql.passward,
        configs.mysql.ip,
        configs.mysql.database,
    ),
    pool_recycle=3600,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
)
