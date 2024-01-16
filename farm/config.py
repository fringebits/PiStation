import json

class Config:
    def __init__(self, fullpath):
        with open(fullpath) as f:
            self.config = json.load(f)

    def get(self, key):
        if key in self.config:
            return self.config[key]
        return None