"""Configuration settings for VersionDB."""
import os
# from apispec.ext.marshmallow import MarshmallowPlugin


class Defaults(object):
    """Parent configuration class."""

    DEBUG                      = True
    CSRF_ENABLED               = True
    SECRET                     = os.getenv('SECRET')
    RESTPLUS_VALIDATE          = True
    RESTPLUS_MASK_SWAGGER      = True
    RESTPLUS_ERROR_404_HELP    = True
    TESTING                    = False
    VERSIONDB_ENABLE_SWAGGER   = os.environ.get("VERSIONDB_ENABLE_SWAGGER", default=True)
    VERSIONDB_ADMIN_USERNAME   = os.environ.get("VERSIONDB_ADMIN_USERNAME", default="admin")
    VERSIONDB_ADMIN_PASSWORD   = os.environ.get("VERSIONDB_ADMIN_PASSWORD", default="password")
    VERSIONDB_SERVICE_NAME     = os.environ.get("VERSIONDB_SERVICE_NAME", default="VersionDB")
    VERSIONDB_SERVICE_HOST     = os.environ.get("VERSIONDB_SERVICE_HOST", default="localhost")
    VERSIONDB_SERVICE_PORT     = os.environ.get("VERSIONDB_SERVICE_PORT", default=5000)
    VERSIONDB_SERVICE_STATUS   = os.environ.get("VERSIONDB_SERVICE_STATUS", default="/api/v1/core/status")
    VERSIONDB_CONFIG_LOG_PATH  = os.environ.get("VERSIONDB_CONFIG_LOG_PATH", default="/app/log")
    VERSIONDB_CONFIG_LOG_LEVEL = os.environ.get("VERSIONDB_CONFIG_LOG_LEVEL", default="INFO")
    VERSIONDB_MONGODB_HOST     = os.environ.get("VERSIONDB_MONGODB_HOST", default="localhost")
    VERSIONDB_MONGODB_PORT     = os.environ.get("VERSIONDB_MONGODB_PORT", default=27017)
    VERSIONDB_MONGODB_USERNAME = os.environ.get("VERSIONDB_MONGODB_USERNAME", default="admin")
    VERSIONDB_MONGODB_PASSWORD = os.environ.get("VERSIONDB_MONGODB_PASSWORD", default="password")
    VERSIONDB_MONGODB_AUTHDB   = os.environ.get("VERSIONDB_MONGODB_AUTHDB", default="admin")
    VERSIONDB_MONGODB_DATABASE = os.environ.get("VERSIONDB_MONGODB_DATABASE", default="database")
    VERSIONDB_MONGODB_URL      = os.environ.get("VERSIONDB_MONGODB_URL", default="")
    JWT_SECRET_KEY             = os.environ.get("JWT_SECRET_KEY", default="CHANGEME")


class developmentConfig(Defaults):
    """Parent configuration class."""
    TESTING                  = True


class ciConfig(Defaults):
    """Parent configuration class."""

    DEBUG                     = True
    TESTING                   = True
    VERSIONDB_CONFIG_LOG_PATH = os.environ.get("VERSIONDB_CONFIG_LOG_PATH", default="/tmp")


class productionConfig(Defaults):
    """Configurations for Production."""

    DEBUG                    = False
    ERROR_404_HELP           = False
    VERSIONDB_ENABLE_SWAGGER = os.environ.get("VERSIONDB_ENABLE_SWAGGER", default=False)


app_config = {
    'development': developmentConfig,
    'ci': ciConfig,
    'test': ciConfig,
    'production': productionConfig,
}
