from flask import json, jsonify
from app.models import Person
from app.classifiers import FoodClassifier

class BaseFormatter():
  def __init__(self, obj):
    self.obj = obj
  
  def build_dict(self):
    pass

  def process(self):
    if not self.obj:
      if type(self.obj) is list:
        return jsonify([])  
      return jsonify({})

    return jsonify(self.build_dict())

  @classmethod
  def format(cls, obj):
    formatter = cls(obj)
    return formatter.process()

class CompanyFormatter(BaseFormatter):
  def build_dict(self):
    return {
      'index': self.obj.index,
      'name': self.obj.name,
      'staff': PeopleFormatter(self.obj.staff).build_dict()
    }

class PersonFormatter(BaseFormatter):
  def build_dict(self):
    return {
      **{
        'username': self.obj.name,
        'age': self.obj.age
      },
      **FoodClassifier(self.obj.favouriteFood).process()
    }
  
class EmplyeeFormatter(BaseFormatter):
  def build_dict(self):
    return {
      'index': self.obj.index,
      "has_died": self.obj.has_died,
      "balance": '${:,.2f}'.format(self.obj.balance),
      "picture": self.obj.picture,
      "age": self.obj.age,
      "eyeColor": self.obj.eyeColor,
      "gender": self.obj.gender,
      "email": self.obj.email,
      "phone": self.obj.phone,
      'username': self.obj.name,
      'age': self.obj.age,
    }

class PersonalInfoFormatter(BaseFormatter):
  def build_dict(self):
    return {
      'name': self.obj.name,
      'age': self.obj.age,
      'address': self.obj.address,
      'phone': self.obj.phone
    }

class PeopleFormatter(BaseFormatter):
  def build_dict(self):
    people_list = []
    for person in self.obj:
      people_list.append(EmplyeeFormatter(person).build_dict())

    return people_list

class FriendsInCommonFormatter(BaseFormatter):
  def build_dict(self):
    return {
      'person_a': PersonalInfoFormatter(self.obj['person_a']).build_dict(),
      'person_b': PersonalInfoFormatter(self.obj['person_b']).build_dict(),
      'friends_in_common': PeopleFormatter(self.obj['friends_in_common']).build_dict()
    }
