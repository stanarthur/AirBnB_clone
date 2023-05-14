#!/usr/bin/python3
"""Module for FileStorage class"""
import datetime
import json
import os


class FileStorage:
    file_path = "file.json"
    objects = {}

    def classes(self):
        """returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review


        classes = {"BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review}
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

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes