from app.models import Person
from app.api import bp
from app.api.errors import error_response
from app.json_formatters import PersonFormatter
from mongoengine.queryset.visitor import Q

@bp.route('/people/<int:id>', methods=['GET'])
def get_person(id):
  person = Person.objects(pk=id).first()
  
  return render_person(person)

def render_person(person):
  if person is None:
    return error_response(404, message='Connot find this person')
  else:
    return PersonFormatter.format(person)
