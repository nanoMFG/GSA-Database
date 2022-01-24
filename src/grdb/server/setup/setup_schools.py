from grdb.database import Base
from grdb.server.app.db import Database
from grdb.server.app.config import Config

admin_db = Database(Base)
admin_db.init(Config.DEV_DATABASE_URL_ADMIN)

# create tables for webapp
from grdb.database.models import User
from grdb.database.models import Institution

# reset user & institution table
User.__table__.drop(admin_db.engine)
Institution.__table__.drop(admin_db.engine)
Base.metadata.create_all(bind=admin_db.engine)

# init school database
import json

file = open('/Users/junelee/gresq/GSA-Database/src/grdb/server/setup/allSchools.json')  # fix url as needed
schools = json.load(file)
schools.sort(key=lambda s: s['name'])
db = admin_db.Session()
i = 1
for school in schools:
    institution = Institution(name=school['name'], country=school['country'])
    db.add(institution)
    if i % 300 == 0:
        db.commit()
        print(i, '/', len(schools), 'done')
    i += 1
db.commit()
print(len(schools), '/', len(schools), 'done')
db.close()
