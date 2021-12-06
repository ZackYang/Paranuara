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
