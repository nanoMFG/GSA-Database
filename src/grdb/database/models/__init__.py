from grdb.database.models.furnace import Furnace
from grdb.database.models.substrate import Substrate
from grdb.database.models.environment_conditions import EnvironmentConditions
from grdb.database.models.recipe import Recipe
from grdb.database.models.preparation_step import PreparationStep
from grdb.database.models.experiment import Experiment
from grdb.database.models.author import Author
from grdb.database.models.sem_file import SemFile
from grdb.database.models.sem_analysis import SemAnalysis
from grdb.database.models.software import Software
from grdb.database.models.raman_file import RamanFile
from grdb.database.models.raman_analysis import RamanAnalysis
from grdb.database.models.properties import Properties
<<<<<<< HEAD

Recipe.maximum_temperature.info["verbose_name"] = "Maximum Temperature"
Recipe.maximum_temperature.info["std_unit"] = "C"

Recipe.maximum_pressure.info["verbose_name"] = "Maximum Pressure"
Recipe.maximum_pressure.info["std_unit"] = "Torr"

Recipe.average_carbon_flow_rate.info["verbose_name"] = "Average Carbon Flow Rate"
Recipe.average_carbon_flow_rate.info["std_unit"] = "sccm"

Recipe.carbon_source.info["verbose_name"] = "Carbon Source"
Recipe.carbon_source.info["std_unit"] = None

Recipe.uses_helium.info["verbose_name"] = "Uses Helium"
Recipe.uses_helium.info["std_unit"] = None

Recipe.uses_argon.info["verbose_name"] = "Uses Argon"
Recipe.uses_argon.info["std_unit"] = None

Recipe.uses_hydrogen.info["verbose_name"] = "Uses Hydrogen"
Recipe.uses_hydrogen.info["std_unit"] = None

Author.full_name_and_institution.info["verbose_name"] = "Author"
Author.full_name_and_institution.info["std_unit"] = None
=======
# from grdb.database.models.user import User
# from grdb.database.models.institution import Institution
>>>>>>> 66ffa44fb0540fb2a9de62147829e9d22221d52a
