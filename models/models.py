from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, MetaData, ForeignKey, Enum, DateTime
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Gun(Base):
    __tablename__ = "gun"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    barrel_type = Column(Enum('Rifled', 'Smoothbore' 'Polygonal', name='barrel_type'), nullable=False)
    caliber = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('gun_category.id'))

    category = relationship('Category', back_populates='guns')


class Category(Base):
    __tablename__ = "gun_category"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)

    guns = relationship('Gun', back_populates='category')


class Ammo(Base):
    __tablename__ = "ammo"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    calibers = Column(String(256), nullable=False)
    amount = Column(Integer, nullable=False)

