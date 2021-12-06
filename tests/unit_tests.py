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
