import logging.config
import os
from api.server.config import getConfig

def verify_loglevel(level="INFO"):
    mylevel = level.upper()
    if mylevel in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
        return mylevel
    else:
        return "INFO"


def verify_logpath(path=None):
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except:
            pass


config = {
   "version": 1,
   "disable_existing_loggers": True,
   "formatters": {
      "fileFormatter": {
              "format": "{\"datetime\": \"%(asctime)s\", \"loglevel\": \"%(levelname)s\", \"module\": \"%(name)s\", \"file\": \"%(module)s\", \"function\": \"%(funcName)s\", \"message\": \"%(message)s\"}",
                          "datefmt": "%Y-%m-%d %H:%M:%S",
                          "class": "logging.Formatter"
      },
      "standard": {
           "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
           "datefmt": "%Y-%m-%dT%H:%M:%S%z"
      }
   },
   "handlers": {
       "standard": {
           "class": "logging.StreamHandler",
           "formatter": "standard"
       },
      "fileHandler": {
        "level": "INFO",
        "filename": "/some/path",
        "formatter": "fileFormatter",
        "class": "logging.FileHandler",
        "mode": "a"
      },
      "auditlog": {
        "level": "INFO",
        "filename": "/some/path",
        "formatter": "fileFormatter",
        "class": "logging.FileHandler",
        "mode": "a"
      }
   },
   "loggers": {
       "": {
           "handlers": ["standard", "fileHandler"],
           "level": logging.INFO
       },
       "auditlog": {
           "handlers": ["auditlog"],
           "level": logging.INFO
       }
   }
}

log_path = getConfig(name="VERSIONDB_CONFIG_LOG_PATH")
log_level = getConfig(name="VERSIONDB_CONFIG_LOG_LEVEL")
verify_logpath(path=log_path)

# Set log configuration coming from 'versiondb' configuration settings.
config["handlers"]["fileHandler"]['filename'] = log_path + '/versiondb.log'
config["handlers"]["fileHandler"]['level'] = verify_loglevel(level=log_level)
config["handlers"]["auditlog"]['filename'] = log_path + '/audit.log'

# Load logging configuration
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
loggerAudit = logging.getLogger("auditlog")
