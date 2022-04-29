from grdb.config import Config
from grdb.database import Base, dal as test_db

config_prefix = "TEST_DATABASE"
config_suffix = "_ADMIN"
conf = Config(prefix=config_prefix, suffix=config_suffix, debug=True, try_secrets=False)
test_db.init_db(conf, privileges={"read": True, "write": True, "validate": True})

dbSpec = {
    "nSubstrates": 4,
    "nAuthors": 12,
    "nRecipes": 8,
    "nFurnaces": 2,
    "nExperiments": 10,
    "listAuthorsPerExperiment": [1, 2, 1, 5, 1, 1, 3, 1, 1, 12],
    "listRecipesPerExperiment": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    "listFurnacesPerExperiment": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    "listSemFilesPerExperiment": [1, 2, 3, 1, 2, 3, 1, 2, 3, 4],
}
