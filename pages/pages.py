import json
with open('config.json') as config:
    c = dict(json.load(config))
    assert 'base_url' in c.keys()

BASE_URL = c['base_url']

class BasePage()