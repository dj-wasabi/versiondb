# import sys
# import os

# currentPath = os.path.dirname(os.path.realpath(__file__))
# rootPath = os.path.join(currentPath, "../..")
# sys.path.append(rootPath)

# from api.server.config import as_dict, getConfig


# def test_server_config_as_dict():
#     config = as_dict()

#     assert config
#     assert config['VERSIONDB_ENVIRONMENT'] == "ci"
#     assert config['TESTING']
#     assert config['VERSIONDB_ADMIN_USERNAME'] == "admin"


# def test_server_config_getConfig():
#     config = getConfig(name="VERSIONDB_ENVIRONMENT")
#     assert config == "ci"

#     no_config = getConfig(name="FLASK_ENV_FLASK")
#     assert no_config is None
