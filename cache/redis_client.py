import redis
from src import config

client = redis.Redis(
    config.get_env(config.EnvKeys.CACHE_REDIS_HOST),
    port=config.get_env(config.EnvKeys.CACHE_REDIS_PORT),
)
