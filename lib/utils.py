"""
utils - a collection of useful methods

2018-0529 PePo new - readjson()
"""
import json

USE_DEBUG = False #

def readjson(jsonfile):
    """readjson(file) - returns the contents of file in JSON-format"""
    with open(jsonfile, 'r') as infile:
        config = json.load(infile)
    if USE_DEBUG:
        print ('JSON: {}'.format(config))
    return config

def readfile(filename):
    """readfile(filename) - returns the contents of file"""
    with open(filename, 'r') as f:
        return (f.read())
