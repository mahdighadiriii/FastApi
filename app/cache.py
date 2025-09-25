import json
from typing import Any

import redis
from fastapi import Depends

from app.database import get_redis


class CacheManager:
    def __init__(self, redis_client: redis.Redis = Depends(get_redis)):
        self.redis = redis_client

    def get(self, key: str) -> Any | None:
        """Retrieve data from cache by key."""
        try:
            cached_data = self.redis.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except redis.RedisError as e:
            print(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: Any, expire_seconds: int = 300) -> bool:
        """Store data in cache with an optional expiration time (in seconds)."""
        try:
            serialized_value = json.dumps(value)
            self.redis.setex(key, expire_seconds, serialized_value)
            return True
        except redis.RedisError as e:
            print(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete data from cache by key."""
        try:
            self.redis.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Redis delete error: {e}")
            return False

    def clear_user_cache(self, user_id: int) -> bool:
        """Clear all cache entries related to a specific user."""
        try:
            cursor = 0
            pattern = f"expenses:{user_id}*"
            while True:
                cursor, keys = self.redis.scan(
                    cursor=cursor, match=pattern, count=100
                )
                if keys:
                    self.redis.delete(*keys)
                if cursor == 0:
                    break
            return True
        except redis.RedisError as e:
            print(f"Redis clear cache error: {e}")
            return False
