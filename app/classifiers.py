import json
import os

def invert_dict(d): 
    inverse = dict() 
    for key in d: 
      for item in d[key]:
