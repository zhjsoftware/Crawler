__author__ = 'jing'

import json
import ConfigParser

configParser = ConfigParser.ConfigParser()

configParser.read('0.ini')

print configParser.get('section','name')