# from api.server.config import as_dict

# def getRedisConfig():
#     currentConfig = as_dict()
#     redisConfig = {}

#     if 'CACHE_REDIS_HOST' in currentConfig:
#         if currentConfig['CACHE_REDIS_HOST'] != '':
#             redisConfig['host'] = currentConfig['CACHE_REDIS_HOST']
#     if 'CACHE_REDIS_PORT' in currentConfig:
#         if currentConfig['CACHE_REDIS_PORT'] != '':
#             redisConfig['port'] = int(currentConfig['CACHE_REDIS_PORT'])
#     if 'CACHE_REDIS_DB' in currentConfig:
#         if currentConfig['CACHE_REDIS_DB'] != '':
#             redisConfig['db'] = currentConfig['CACHE_REDIS_DB']
#     if 'CACHE_REDIS_PASSWORD' in currentConfig:
#         if currentConfig['CACHE_REDIS_PASSWORD'] != '':
#             redisConfig['password'] = currentConfig['CACHE_REDIS_PASSWORD']
#     if 'CACHE_DEFAULT_TIMEOUT' in currentConfig:
#         if currentConfig['CACHE_DEFAULT_TIMEOUT'] != '':
#             redisConfig['socket_timeout'] = int(currentConfig['CACHE_DEFAULT_TIMEOUT'])

#     return redisConfig
