from app import create_app, db, classifiers
from app.models import Company, Person

app = create_app()

print('Start loading data from json files')
Company.import_from_json()
Person.import_from_json()
print('Loading completed')