from app import create_app, db, classifiers
from app.models import Company, Person

app = create_app()

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'Company': Company, 'Person': Person, 'classifiers': classifiers}
