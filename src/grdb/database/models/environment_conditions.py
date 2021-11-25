from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from grdb.database import Base


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

    def json(self):
        return {
            'id': self.id,
            'dew_point': self.dew_point,
            'ambient_temperature': self.ambient_temperature
        }

    def json_encodable(self):
        params = [
            "dew_point",
            "ambient_temperature",
        ]
        json_dict = {'id': self.id}
        for p in params:
            info = getattr(EnvironmentConditions, p).info
            json_dict[p] = {
                "value": getattr(self, p),
                "unit": info["std_unit"] if "std_unit" in info else None,
            }
        return json_dict
