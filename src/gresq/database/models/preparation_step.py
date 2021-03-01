from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from gresq.database import Base


class PreparationStep(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    # Basic integer primary key
    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    # The recipe can be the same for multiple different preparation steps
    recipe_id = Column(
        Integer,
        ForeignKey("recipe.id", ondelete="CASCADE"),
        info={"verbose_name": "Recipe ID"},
        index=True,
    )

    # MANY-TO-ONE: preparation_steps->recipe
    #recipe = relationship("Recipe", uselist=False, back_populates="preparation_steps")
    recipe = relationship("Recipe", back_populates="preparation_steps")

    step = Column(Integer) # Should this be renamed to "step_number"?
    name = Column(
        String(16),
        info={
            "verbose_name": "Name",
            "choices": ["Annealing", "Growing", "Cooling"],
            "required": True,
        },
    )
    duration = Column(
        Float,
        info={
            "verbose_name": "Duration",
            "std_unit": "min",
            "conversions": {"min": 1, "sec": 1 / 60.0, "hrs": 60},
            "required": True,
            "tooltip": "Duration of the step",
        },
    )
    furnace_temperature = Column(
        Float,
        info={
            "verbose_name": "Furnace Temperature",
            "std_unit": "C",
            "conversions": {"C": 1},
            "required": True,
            "tooltip": "Temperature of the furnace during the step",
        },
    )
    furnace_pressure = Column(
        Float,
        info={
            "verbose_name": "Furnace Pressure",
            "std_unit": "Torr",
            "conversions": {
                "Torr": 1,
                "Pa": 1 / 133.322,
                "mbar": 1 / 1.33322,
                "mTorr": 1.0e-3,
            },
            "required": True,
            "tooltip": "Pressure in the furnace during the step",
        },
    )
    sample_location = Column(
        Float,
        info={
            "verbose_name": "Sample Location",
            "std_unit": "mm",
            "conversions": {"inches": 25.4, "mm": 1},
            "required": False,
            "tooltip": "Position of the sample in the tube",
        },
    )
    helium_flow_rate = Column(
        Float,
        info={
            "verbose_name": "Helium Flow Rate",
            "std_unit": "sccm",
            "conversions": {"sccm": 1},
            "required": False,
            "tooltip": "Leave blank if helium was not used",
        },
    )
    hydrogen_flow_rate = Column(
        Float,
        info={
            "verbose_name": "Hydrogen Flow Rate",
            "std_unit": "sccm",
            "conversions": {"sccm": 1},
            "required": False,
            "tooltip": "Leave blank if hydrogen was not used",
        },
    )
    carbon_source_flow_rate = Column(
        Float,
        info={
            "verbose_name": "Carbon Source Flow Rate",
            "std_unit": "sccm",
            "conversions": {"sccm": 1},
            "required": True,
        },
    )
    argon_flow_rate = Column(
        Float,
        info={
            "verbose_name": "Argon Flow Rate",
            "std_unit": "sccm",
            "conversions": {"sccm": 1},
            "required": False,
            "tooltip": "Leave blank if argon was not used",
        },
    )
    cooling_rate = Column(
        Float,
        info={
            "verbose_name": "Cooling Rate",
            "std_unit": "C/min",
            "conversions": {"C/min": 1},
            "required": False,
        },
    )
