#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import Company, Person
from app.classifiers import FoodClassifier
from config import Config
from mongoengine import connect
import os
import json
from decimal import Decimal
import requests


class TestConfig(Config):
    TESTING = True
    MONGODB_DB = 'paranuara_test'


class ApiTest(unittest.TestCase):

  def setUp(self):
    self.app = create_app(TestConfig)
    self.client = self.app.test_client()
    self.db = db.get_db()
    Company.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'companies.json'))
    Person.import_from_json(os.path.join(os.getcwd(), 'tests', 'fixtures', 'people.json'))

  def tearDown(self):
    # Delete Database collections after the test is complete
    for collection in self.db.list_collection_names():
        self.db.drop_collection(collection)

  def test_successful_found_company(self):
    # When
    response = self.client.get(
        '/api/companies/1', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(1, response.json['index'])
    self.assertEqual('PERMADYNE', response.json['name'])
    self.assertEqual(2, len(response.json['staff']))
    self.assertEqual(200, response.status_code)

  def test_failed_found_company(self):
    # When
    response = self.client.get('/api/companies/9', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(404, response.status_code)
    self.assertEqual('Your company id is incorrect',
                      response.json['message'])

  def test_successful_get_friends_in_common(self):
    # When
    response = self.client.get('/api/friends_in_common/3-4/with/brown/eyes', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(200, response.status_code)
    self.assertEqual('Rosemary Hayes', response.json['person_a']['name'])
    self.assertEqual('Mindy Beasley', response.json['person_b']['name'])
    self.assertEqual(1, len(response.json['friends_in_common']))
    self.assertEqual('Bonnie Bass', response.json['friends_in_common'][0]['username'])

  def test_failed_get_friends_in_common(self):
    # When
    response = self.client.get('/api/friends_in_common/9-4/with/brown/eyes', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(404, response.status_code)

  def test_successful_get_person(self):
    # When
    response = self.client.get('/api/people/1', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(200, response.status_code)
    self.assertEqual(["cucumber"], response.json['fruits'])
    self.assertEqual(["beetroot", "carrot", "celery"], response.json['vegetables'])
    self.assertEqual(60, response.json['age'])
    self.assertEqual('Decker Mckenzie', response.json['username'])

  def test_failed_get_friends_in_common(self):
    # When
    response = self.client.get('/api/people/999', headers={"Content-Type": "application/json"})

    # Then
    self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main(verbosity=2)
