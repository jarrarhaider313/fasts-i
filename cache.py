from cachetools import TTLCache

user_cache = TTLCache(maxsize=60,ttl=50)

task_cache= TTLCache(maxsize=60,ttl=50)