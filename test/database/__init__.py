import os

from gresq.config import Config
from grdb.database.v1_1_0 import dal

# Testing Configuration and dal initialization
config_prefix = "TEST_DATABASE"
config_suffix = "_ADMIN"
conf = Config(prefix=config_prefix, suffix=config_suffix, debug=True, try_secrets=False)
dal.init_db(conf, privileges={"read": True, "write": True, "validate": True})
