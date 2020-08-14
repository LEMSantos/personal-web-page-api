from orator import DatabaseManager
from config.database import DATABASES
from orator import Model
import env

DATABASES['sqlite']['database'] = env.DATABASE

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)
