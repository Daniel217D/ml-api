from dependency_injector import containers, providers
from redis.asyncio import Redis

from api.config import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    redis = providers.Singleton(
        Redis.from_url,
        settings.provided.redis_url,
        decode_responses=True,
    )
