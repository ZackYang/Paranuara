import json
import os

def invert_dict(d): 
    inverse = dict() 
    for key in d: 
      for item in d[key]:
        inverse[item] = key
    return inverse

class BaseClassifier:
  def __init__(self, data):
    self.oringinal_data = data

  def process():
    return {}

class FoodClassifier(BaseClassifier):
  food_tables = ['vegetables', 'fruits']
  food_mapping = {}
  for food_type in food_tables:
    json_path = os.path.join(os.getcwd(), 'classifier_data', food_type + '.json')
    food_mapping[food_type] = json.load(open(json_path))[food_type]
  food_mapping = invert_dict(food_mapping)

  def __rule(self, food):
    if food in FoodClassifier.food_mapping:
      return FoodClassifier.food_mapping[food]
    else:
      print("Unknown Food %s" % food)
      return 'UnknownFood'

  def process(self):
    result = {}
    for food_type in FoodClassifier.food_tables:
      result[food_type] = []

    for food in self.oringinal_data:
      food_type = self.__rule(food)
      if food_type in result:
        result[food_type].append(food)
    
    return result
