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

