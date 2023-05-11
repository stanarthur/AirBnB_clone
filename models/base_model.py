#!/usr/bin/python3
"""Module for base class which
contains the base class for the AirBnB clone console.
"""

import uuid
from datetime import datetime



class BaseModel:
    
    """updates the instance of the instance BaseModel"""

    def __init__(self, *args, **kwargs ):

        """**Kwargs and *args:
        *args: list of arguments.
        **kwargs: dict of key/value arguments
        """

        if kwargs is not None and kwargs != {}:
            for data_key in kwargs:
                if data_key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif data_key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[data_key] = kwargs[data_key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

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

