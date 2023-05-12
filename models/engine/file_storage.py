#!/usr/bin/python3
"""Module for FileStorage class"""
import datetime
import json
import os


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """intializes new_obj in __objects dictionary."""
        key = "{}.{}". format(type(obj).__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to JSON file"""
        serial_objects = {}
        for s_key, s_obj in self.__objects.items():
            serial_objects[s_key] = s_obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(serial_objects, file)

    def reload(self):
        """Deserializes JSON file into __objects."""
        if not os.path.isfile(self.__file_path):
            return
        with open(self.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {key: self.classes()[value["__class__"]](**value)
                        for key, value in obj_dict.items()}
            self.__objects = obj_dict
