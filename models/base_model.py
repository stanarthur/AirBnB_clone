#!/usr/bin/python3
"""Module for Base class which
contains the Base class for the AirBnB clone console.
"""

import uuid
from datetime import datetime
#from models import storage


class BaseModel:
    """
    BaseModel class that defines all common attributes/methods for
    other classes
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor of BaseModel instance

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime
                            (value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            #storage.new(self)

    def __str__(self):
        """
        Method that returns string representation of the BaseModel instance
        """
        return "[{}] ({}) {}".\
            format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Method that updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        #storage.save()

    def to_dict(self):
        """
        Method that returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()

        return obj_dict
