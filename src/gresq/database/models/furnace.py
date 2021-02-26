# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:57:13 2021

@author: Mitisha Surana
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from gresq.database import Base

class Furnace(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    # Basic integer primary key
    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    # MANY-TO-ONE: furnace->sample
    sample = relationship("Sample", back_populates="Furnace")

    tube_diameter = Column(
        Float,
        info={
            "verbose_name": "Tube Diameter",
            "std_unit": "mm",
            "conversions": {"mm": 1, "inches": 25.4},
            "required": False,
            "tooltip": "Diameter of the furnace tube",
        },
    )
    cross_sectional_area = Column(
        Float,
        info={
            "verbose_name": "Cross-sectional area",
            "std_unit": "mm2",
            "conversions": {"mm2": 1, "inch2": 645.16},
            "required": False,
        },
    )
    tube_length = Column(
        Float,
        info={
            "verbose_name": "Tube length",
            "std_unit": "mm",
            "conversions": {"mm": 1, "inches": 25.4},
            "required": False,
            "tooltip": "Length of the furnace tube",
        },
    )
    # length_of_heated_region = Column(
    #     Float,
    #     info={
    #         "verbose_name": "Length of heated region",
    #         "std_unit": "mm",
    #         "conversions": {"inches": 25.4, "mm": 1},
    #         "required": False,
    #         "tooltip": "Length of the part of the furnace with the growth temperature",
    #     },
    # )
    