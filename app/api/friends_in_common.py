from app.models import Person
from app.api import bp
from app.api.errors import error_response
from app.json_formatters import FriendsInCommonFormatter
from mongoengine.queryset.visitor import Q

@bp.route('/friends_in_common/<int:a_id>-<int:b_id>/with/<string:color>/eyes', methods=['GET'])
def get_friends_in_common(a_id, b_id, color):
  person_a = Person.objects(pk=a_id).first()
  person_b = Person.objects(pk=b_id).first()

  return render_friends_in_common(person_a, person_b, eyeColor=color, has_died=False)

def render_friends_in_common(person_a, person_b, **other_query):
  if person_a is None or person_b is None:
    return error_response(404, message='Connot find this person')
  else:
    result = {
      'person_a': person_a,
      'person_b': person_b,
      'friends_in_common': Person.friends_in_common(person_a, person_b, **other_query)
    }
    return FriendsInCommonFormatter.format(result)
