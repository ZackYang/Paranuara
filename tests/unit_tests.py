#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import Company, Person
from app.classifiers import FoodClassifier
from config import Config
from mongoengine import connect
import os
from decimal import Decimal


class TestConfig(Config):
  TESTING = True
  MONGODB_DB = 'paranuara_test'

class CompanyModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    Company.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'companies.json'))

  def tearDown(self):
    db = connect('paranuara_test')
    db.drop_database('paranuara_test')
    self.app_context.pop()

  def test_import_from_json(self):
    Company.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'companies.json'))
    self.assertEqual(Company.objects().count(), 6)
    self.assertEqual(Company.objects(pk=0).first().name, 'NETBOOK')

class PersonModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    Company.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'companies.json'))

  def tearDown(self):
    db = connect('paranuara_test')
    db.drop_database('paranuara_test')
    self.app_context.pop()

  def test_build_from_json(self):
    person = Person.build_from_json({
      "_id": "595eeb9b96d80a5bc7afb106",
      "index": 0,
      "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
      "has_died": True,
      "balance": "$2,418.59",
      "picture": "http://placehold.it/32x32",
      "age": 61,
      "eyeColor": "blue",
      "name": "Carmella Lambert",
      "gender": "female",
      "company_id": 2,
      "email": "carmellalambert@earthmark.com",
      "phone": "+1 (910) 567-3630",
      "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
      "about": "Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur. Cupidatat labore incididunt nostrud exercitation ullamco reprehenderit dolor eiusmod sit exercitation est. Voluptate consectetur est fugiat magna do laborum sit officia aliqua magna sunt. Culpa labore dolore reprehenderit sunt qui tempor minim sint tempor in ex. Ipsum aliquip ex cillum voluptate culpa qui ullamco exercitation tempor do do non ea sit. Occaecat laboris id occaecat incididunt non cupidatat sit et aliquip.\r\n",
      "registered": "2016-07-13T12:29:07 -10:00",
      "tags": [
        "id",
        "quis",
        "ullamco",
        "consequat",
        "laborum",
        "sint",
        "velit"
      ],
      "friends": [
        {
          "index": 0
        },
        {
          "index": 1
        },
        {
          "index": 2
        }
      ],
      "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
      "favouriteFood": [
        "orange",
        "apple",
        "banana",
        "strawberry"
      ]
    })
    self.assertEqual(str(person.balance), '2418.59')
    self.assertEqual(str(person.customer_id), '595eeb9b96d80a5bc7afb106')
    self.assertEqual(person.name, 'Carmella Lambert')
    self.assertEqual(person.pk, 0)
    self.assertEqual(person.email, "carmellalambert@earthmark.com")
    self.assertEqual(person.company, Company.objects(pk=2).first())

  def test_import_from_json(self):
    Person.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))
    self.assertEqual(Person.objects().count(), 5)

  def test_update_friends_companies_from_json(self):
    # Prepare data
    Person.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))
    
    # Update
    Person.update_friends_companies_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))

    # Result
    person = Person.objects(index=0).first()
    self.assertEqual(len(person.friends), 4)
    self.assertTrue(Person.objects(pk=3).first() in person.friends)
    self.assertFalse(Person.objects(pk=4).first() in person.friends)
    
    company = Company.objects(pk=1).first()
    self.assertEqual(len(company.staff), 2)

  def test_friends_in_common(self):
    # Prepare data
    Person.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))
    Person.update_friends_companies_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))

    person_a = Person.objects(pk=3).first()
    person_b = Person.objects(pk=4).first()

    # Query
    friends = Person.friends_in_common(person_a, person_b)
    self.assertEqual(len(friends), 2)
    self.assertTrue(Person.objects(pk=1).first() in friends)
    self.assertTrue(Person.objects(pk=2).first() in friends)

    friends = Person.friends_in_common(person_a, person_b, eyeColor='brown')
    self.assertEqual(len(friends), 1)
    self.assertFalse(Person.objects(pk=1).first() in friends)
    self.assertTrue(Person.objects(pk=2).first() in friends)

class FoodClassifierCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    
  def tearDown(self):
    db = connect('paranuara_test')
    db.drop_database('paranuara_test')
    self.app_context.pop()

  def test_process(self):
    result = FoodClassifier(["cabbage", "calabrese", "caraway", "apple"]).process()
    
    self.assertTrue(result['fruits'] == ['apple'])
    self.assertTrue(result['vegetables'] == ["cabbage", "calabrese", "caraway"])

if __name__ == '__main__':
  unittest.main(verbosity=2)
