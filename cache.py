import hashlib
import json
from typing import Optional
import redis
from backend.utils.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Redis client
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def _make_key(raw: str) -> str:
    digest = hashlib.sha256(raw.encode("utf-8", errors="ignore")).hexdigest()
    return f"analysis:{digest}"


def get_cached_analysis(key: str) -> Optional[dict]:
    cache_key = _make_key(key)
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info("Cache hit", extra={"key": cache_key[:10]})
            return json.loads(cached_data)
        logger.info("Cache miss", extra={"key": cache_key[:10]})
        return None
    except Exception as e:
        logger.warning("Cache retrieval failed", extra={"error": str(e)})
        return None


def set_cached_analysis(key: str, value: dict, ttl: int = None) -> None:
    if ttl is None:
        ttl = settings.CACHE_TTL_SECONDS
    cache_key = _make_key(key)
    try:
        redis_client.setex(cache_key, ttl, json.dumps(value))
        logger.info("Cached analysis result", extra={"key": cache_key[:10], "ttl": ttl})
    except Exception as e:
        logger.warning("Cache storage failed", extra={"error": str(e)})
