# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:08:39 2021

@author: Mitisha Surana
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from gresq.database import Base


class Substrate(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    # Basic integer primary key
    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})
    
    # MANY-TO-ONE: substrate->experiment
    experiments = relationship("Experiment", back_populates="substrate")

    catalyst = Column(
        String(16),
        info={
            "verbose_name": "Catalyst",
            "choices": ["Copper", "Palladium", "Platinum", "Other"],
            "required": True,
        },
    )
    thickness = Column(
        Float,
        info={
            "verbose_name": "Thickness",
            "std_unit": "um",
            "conversions": {"um": 1, "nm": 1 / 1000.0, "mm": 1000.0},
            "required": True,
            "tooltip": "Thickness of the catalyst used",
        },
    )
    diameter = Column(
        Float,
        info={
            "verbose_name": "Diameter",
            "std_unit": "mm",
            "conversions": {"mm": 1, "um": 1 / 1000.0, "cm": 10.0},
            "required": False,
            "tooltip": "Diameter of the substrate",
        },
    )
    length = Column(
        Float,
        info={
            "verbose_name": "Length",
            "std_unit": "mm",
            "conversions": {"mm": 1, "um": 1 / 1000.0, "cm": 10.0},
            "required": False,
            "tooltip": "Length of the substrate",
        },
    )
    surface_area= Column(
        Float,
        info={
            "verbose_name": "Sample Surface Area",
            "std_unit": "mm2",
            "conversions": {"mm2": 1, "um2": 1 / 10.0**6, "cm2": 100.0},
            "required": False,
            "tooltip": "Surface area of the substrate",
        },
    )