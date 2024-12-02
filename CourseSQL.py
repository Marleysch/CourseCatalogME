from typing import List
from orm_base import Base
from sqlalchemy import String, CheckConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Course(Base):
    __tablename__ = 'course'

    # course: choices = ['Department Abbreaviate]
    name: Mapped[str] = mapped_column(String(80), CheckConstraint("LENGTH(name) >= 1", name="name_length"),
                                      primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String(80), CheckConstraint("LENGTH(name) >= 1", name="name_length"),
                                             primary_key=True, nullable=False)

    unit: Mapped[int] = mapped_column(Integer, CheckConstraint("unit >= 1 AND unit <= 5", name="credit_value"),
                                      primary_key=True, nullable=False)

    # Relationship to General and
    '''
    generals: Mapped[List['Schedule']] = relationship("Schedule", back_populates='shift',
                                                       cascade='all, save-update, delete-orphan')
                                                       
    '''
    def __init__(self, name: str, description: str, units: int, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.units = units

    def __str__(self):
        return f'{self.name}: {self.description} Units: {self.units}'
