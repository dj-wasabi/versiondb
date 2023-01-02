from api.server.config import as_dict

def getMongoConfig():
    currentConfig = as_dict()
    mongoDbConfig = {}

    if 'VERSIONDB_MONGODB_HOST' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_HOST'] != '':
            mongoDbConfig['host'] = currentConfig['VERSIONDB_MONGODB_HOST']
    if 'VERSIONDB_MONGODB_PORT' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_PORT'] != '':
            mongoDbConfig['port'] = currentConfig['VERSIONDB_MONGODB_PORT']
    if 'VERSIONDB_MONGODB_USERNAME' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_USERNAME'] != '':
            mongoDbConfig['username'] = currentConfig['VERSIONDB_MONGODB_USERNAME']
    if 'VERSIONDB_MONGODB_PASSWORD' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_PASSWORD'] != '':
            mongoDbConfig['password'] = currentConfig['VERSIONDB_MONGODB_PASSWORD']
    if 'VERSIONDB_MONGODB_AUTHDB' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_AUTHDB'] != '':
            mongoDbConfig['authSource'] = currentConfig['VERSIONDB_MONGODB_AUTHDB']
    if 'VERSIONDB_MONGODB_URL' in currentConfig:
        if currentConfig['VERSIONDB_MONGODB_URL'] != '':
            mongoDbConfig['url'] = currentConfig['VERSIONDB_MONGODB_URL']

    return mongoDbConfig
