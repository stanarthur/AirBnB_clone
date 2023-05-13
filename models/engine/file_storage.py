#!/usr/bin/python3
"""Module for FileStorage class"""
import datetime
import json
import os


class FileStorage:
    file_path = "file.json"
    objects = {}

    def classes(self):
        """returns a dictionaryof valid classesn and their references"""
        from models.base_model import BaseModel
        from models.user import User

        classes = {"BaseModel": BaseModel,
                "User": User}
        return classes

    def all(self):
        """returns the dictionary __objects."""
        return FileStorage.objects

    def new(self, obj):
        """intializes new_obj in __objects dictionary."""
        key = "{}.{}". format(type(obj).__name__, obj.id)
        FileStorage.objects[key] = obj

    def save(self):
        """serializes __objects to JSON file"""
        serial_objects = {}
        for s_key, s_obj in FileStorage.objects.items():
            serial_objects[s_key] = s_obj.to_dict()
        with open(FileStorage.file_path, "w", encoding="utf-8") as jfile:
            json.dump(serial_objects, jfile)

    def reload(self):
        """deserializes JSON file into __objects."""
        if not os.path.isfile(FileStorage.file_path):
            return
        with open(FileStorage.file_path, "r", encoding="utf-8") as jfile:
            obj_dict = json.load(jfile)
            obj_dict = {key: self.classes()[value["__class__"]](**value)
                    for key, value in obj_dict.items()}
            FileStorage.objects = obj_dict
    