#!/usr/bin/python3
"""Place Module for HBNB project."""
from models.base_model import BaseModel, Base
import models
from models.amenity import Amenity
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import getenv, environ

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id",
                             String(60),
                             ForeignKey("places.id"),
                             primary_key=True),
                      Column("amenity_id",
                             String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True))


class Place(BaseModel, Base):
    """A place to stay."""

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
    else:
        @property
        def reviews(self):
            """Getter attribute reviews that returns the list of Review.
            instances with place_id equals to the current Place.id.
            """
            review_list = []
            from models.review import Review
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, backref="place_amenities")
    else:
        @property
        def amenities(self) -> list:
            """Return the list of amenities instance.
            The amenities instance returned is based on the
            amenities id stored on the list variable amenity_ids.
            """
            amenities_list = []
            for amenity in models.storage.all(Amenity).values():
                for ids in self.amenity_ids:
                    if ids == amenity.id:
                        amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj: Amenity):
            """Add the amenity obj instance id to amenity_ids."""
            if type(obj) != Amenity or obj is None:
                return
            else:
                self.amenity_ids.append(obj.id)
