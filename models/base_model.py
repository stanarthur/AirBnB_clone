#!/usr/bin/python3
"""Module for base class which
contains the base class for the AirBnB clone console.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    
    """updates the instance of the instance BaseModel"""

    def __init__(self, *args, **kwargs ):

        """**Kwargs and *args:
        *args: list of arguments.
        **kwargs: dict of key/value arguments (updated)
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """str function returns string representation
        of BaseModel instance
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """save function updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """to_dict function returns a dictionary
        containing all keys and values of __dict__
        of the instance
        """
        data_dict = self.__dict__.copy()
        data_dict["__class__"] = type(self).__name__
        data_dict["created_at"] = self.created_at.isoformat()
        data_dict["updated_at"] = self.updated_at.isoformat()
        return data_dict

