import redis
import json

class CacheService:
    def __init__(self, cache_url: str):
        self.redis = redis.Redis.from_url(cache_url)

    def get_price(self, product_id: str):
        return self.redis.get(product_id)

    def set_price(self, product_id: str, price: float):
        self.redis.set(product_id, json.dumps(price))
