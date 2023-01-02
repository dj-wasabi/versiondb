import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(currentPath, "../..")
sys.path.append(rootPath)

from api.server.logging import verify_loglevel


def test_server_logging_verify_logpath():
    config = verify_loglevel(level="INFO")
    assert config == "INFO"

    config = verify_loglevel(level="Info")
    assert config == "INFO"

    config = verify_loglevel(level="WARNING")
    assert config == "WARNING"

    # Test non existing level
    config = verify_loglevel(level="infoo")
    assert config == "INFO"
