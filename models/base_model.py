#!/usr/bin/python3
"""
This module contains the BaseModel class:
All classes should inherit from this class
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import models

if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The base class for all storage objects in this project"""

    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False,
                            onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize class object

        Args:
            kwargs: a dictionary containing object attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at'):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at attribute and save the instance"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the object"""
        obj_dict = self.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict

    def __str__(self):
        """Return a string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.to_dict())
