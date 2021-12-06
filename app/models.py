import json
import os
import bson
import re
from app import db
from decimal import Decimal
from mongoengine import signals, CASCADE
from mongoengine.errors import ValidationError
from mongoengine.queryset.visitor import Q

class Company(db.Document):
  name = db.StringField(required=True, unique=True)
  index = db.IntField(required=True, primary_key=True)
  staff = db.ListField(db.ReferenceField('Person'))

  @classmethod
  def import_from_json(cls, json_path=None):
    if json_path is None:
      json_path = os.path.join(os.getcwd(), 'companies.json')

    data = json.load(open(json_path))
    for company_obj in data:
      company = cls(name=company_obj['company'], index=company_obj['index'])
      try:
        company.save()
      except Exception as e:
        print("Error \n %s" % (e))

class Person(db.Document):
  index = db.IntField(required=True, primary_key=True)
  customer_id = db.ObjectIdField(db_field='id', unique=True, default=lambda: bson.objectid.ObjectId())
  guid = db.UUIDField(required=True, unique=True)
  name = db.StringField(required=True)
  has_died = db.BooleanField()
  balance = db.DecimalField(precision=2)
  picture = db.URLField()
  age = db.IntField()
  eyeColor = db.StringField()
  name = db.StringField()
  gender = db.StringField()
  company = db.ReferenceField('Company')
  email = db.EmailField()
  phone = db.StringField()
  address = db.StringField()
  about = db.StringField()
  greeting = db.StringField()
  tags = db.ListField(db.StringField())
  registered = db.DateTimeField()
  favouriteFood = db.ListField()
  friends = db.SortedListField(db.ReferenceField('self', reverse_delete_rule=CASCADE))

  @classmethod
  def friends_in_common(cls, person_a, person_b, **other_query):
    query = Q(index__in = person_a.to_mongo()['friends']) & Q(index__in = person_b.to_mongo()['friends'])
    if other_query:
      query = query & Q(**other_query)

    return cls.objects(query)

  @classmethod
  def build_from_json(cls, json_obj):
    json_obj['company'] = Company.objects(pk = json_obj['company_id']).first()
    json_obj['customer_id'] = json_obj['_id']
    json_obj['balance'] = Decimal(re.sub(r'[\$\,]', '', json_obj['balance']))
    
    json_obj.pop('company_id', None)
    json_obj.pop('friends', None)
    json_obj.pop('_id', None)

    return cls(**json_obj)

  @classmethod
  def import_from_json(cls, json_path=None):
    # Please import the Company data firstly
    if json_path is None:
      json_path = os.path.join(os.getcwd(), 'people.json')
    
    file = open(json_path)
    data = json.load(file)
    file.close()

    for person_obj in data:
      person = cls.build_from_json(person_obj)
      person.save()
      
    cls.update_friends_companies_from_json(json_path)

  @classmethod
  def update_friends_companies_from_json(cls, json_path=None):
    if json_path is None:
      json_path = os.path.join(os.getcwd(), 'people.json')

    data = json.load(open(json_path))
    companie_staffs = {}

    for person_obj in data:
      # Fetch friends list
      person = cls.objects(pk=person_obj['index']).first()
      friends = cls.objects(Q(pk__in = map(lambda friend_obj: friend_obj['index'], person_obj['friends'])))

      person.friends = friends
      person.save()

      # Fetch all companies' staff lists
      if person.company is not None:
        company_name = person.company.name
        if company_name in companie_staffs:
          companie_staffs[company_name].append(person)
        else:
          companie_staffs[company_name] = [person]
    
    # Update companies' staff
    for company_name, staff in companie_staffs.items():
      company = Company.objects(name=company_name).get()
      company.staff = staff
      company.save()


