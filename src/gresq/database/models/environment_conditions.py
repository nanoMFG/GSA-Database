from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from gresq.database import Base

class EnvironmentConditions(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    # Basic integer primary key
    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    # MANY-TO-ONE: environment_conditions->sample
    experiments = relationship("Experiment", back_populates="environment_conditions")

    dew_point = Column(
        Float,
        info={
            "verbose_name": "Dew Point",
            "std_unit": "C",
            "conversions": {"C": 1},
            "required": False,
            "tooltip": "Dew point of the ambient environment",
        },
    )
    ambient_temperature = Column(
        Float,
        info={
            "verbose_name": "Ambient Temperature",
            "std_unit": "C",
            "conversions": {"C": 1},
            "required": False,
            "tooltip": "Temperature of the ambient environment",
        },
    )
    