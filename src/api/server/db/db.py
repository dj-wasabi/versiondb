# import msgpack
# import redis
# import fakeredis
# from api.server.db import getRedisConfig
# from api.server.config import getConfig

# cacheType = getConfig(name="CACHE_TYPE")
# if cacheType == "redis":
#     configSettings = getRedisConfig()
#     db = redis.Redis(**configSettings)
# elif cacheType == "fake":
#     db = fakeredis.FakeStrictRedis(db=1)
# else:
#     db = None


# class DB:
#     """My DB Class."""

#     def __init__(self, db=db, key=None) -> None:
#         self._db = db
#         self.key = key

#     def get(self):
#         """Get the information from an 'key'."""
#         if self._db.exists(self.key):
#             data = self._db.get(self.key)
#             return msgpack.unpackb(data)
#         else:
#             return {}

#     def set(self, data=None):
#         """Write information to an 'key' in the database."""
#         if data is None:
#             data = {}
#         self._db.set(self.key, msgpack.packb(data))

#     def delete(self):
#         """Delete a 'key' from the database."""
#         if self._db.exists(self.key):
#             self._db.delete(self.key)
