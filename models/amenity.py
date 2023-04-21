#!/usr/bin/python3
"""State Module for HBNB project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class for orm mapping."""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    # places = relationship("Place", secondary=association_table,
    #                       backref="amenities")
