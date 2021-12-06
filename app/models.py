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
