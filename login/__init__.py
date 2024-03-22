import flask_jwt_extended
import redis

from src import config

jwt = flask_jwt_extended.JWTManager()


jwt_redis_blocklist = redis.StrictRedis(
    host=config.get_env(config.EnvKeys.CACHE_REDIS_HOST),
    port=config.get_env(config.EnvKeys.CACHE_REDIS_PORT),
    db=0,
    decode_responses=True,
)
