from grdb.config import Config
from grdb.database import Base, dal as test_db

config_prefix = "TEST_DATABASE"
config_suffix = "_ADMIN"
conf = Config(prefix=config_prefix, suffix=config_suffix, debug=True, try_secrets=False)
test_db.init_db(conf, privileges={"read": True, "write": True, "validate": True})
