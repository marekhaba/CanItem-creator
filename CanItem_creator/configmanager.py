"""
Used for config managment
"""
import json

class _ConfigManager:
    __default_values = {
        "theme": "darkTKC",
        "canvas_name": "ca",
    }

    def __init__(self):
        self.__values = {}

    def set(self, item, value):
        self.__values[item] = value
        self.save()

    def get(self, item):
        try:
            return self.__values[item]
        except KeyError:
            return self.__default_values[item]

    def save(self, path="config.json"):
        with open(path, "w") as file:
            json.dump(self.__values, file)

    def load(self, path="config.json"):
        try:
            with open(path, "r") as file:
                self.__values.update(json.load(file))
        except FileNotFoundError:
            return

ConfigManager = _ConfigManager()
