from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, text, and_
from sqlalchemy.sql import exists

from gresq.database import Base, class_registry


class Recipe(Base):
    # Basic integer primary key
    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    carbon_source = Column(
        String(16),
        info={
            "verbose_name": "Carbon Source",
            "choices": ["CH4", "C2H4", "C2H2", "C6H6"],
            "required": True,
        },
    )

    # ONE-TO-MANY: recipe -> preparation_step
    preparation_steps = relationship(
        "PreparationStep",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="recipe",
    )
    # ONE-TO-MANY: recipe -> sample
    samples = relationship(
        "Sample",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="recipe",
    )

    @hybrid_property
    def maximum_temperature(self):
        return max(
            [
                p.furnace_temperature
                for p in self.preparation_steps
                if p.furnace_temperature != None
            ]
        )

    @maximum_temperature.expression
    def maximum_temperature(cls):
        PreparationStep = class_registry["PreparationStep"]
        return (
            select([func.max(PreparationStep.furnace_temperature)])
            .where(PreparationStep.recipe_id == cls.id)
            .correlate(cls)
            .label("maximum_temperature")
        )

    @hybrid_property
    def maximum_pressure(self):
        return max(
            [
                p.furnace_pressure
                for p in self.preparation_steps
                if p.furnace_pressure != None
            ]
        )

    @maximum_pressure.expression
    def maximum_pressure(cls):
        PreparationStep = class_registry["PreparationStep"]
        return (
            select([func.max(PreparationStep.furnace_pressure)])
            .where(PreparationStep.recipe_id == cls.id)
            .correlate(cls)
            .label("maximum_pressure")
        )

    @hybrid_property
    def average_carbon_flow_rate(self):
        steps = [
            p.carbon_source_flow_rate
            for p in self.preparation_steps
            if p.carbon_source_flow_rate != None
        ]
        return sum(steps) / len(steps)

    @average_carbon_flow_rate.expression
    def average_carbon_flow_rate(cls):
        PreparationStep = class_registry["PreparationStep"]
        return (
            select([func.avg(PreparationStep.carbon_source_flow_rate)])
            .where(PreparationStep.recipe_id == cls.id)
            .correlate(cls)
            .label("average_carbon_flow_rate")
        )

    # NOTE: This is really the carbon source from the first step.
    # Should there be a contraint that the carbon source is the same for all steps??
    # @hybrid_property
    # def carbon_source(self):
    #     vals = [
    #         p.carbon_source
    #         for p in self.preparation_steps
    #         if p.carbon_source is not None
    #     ]
    #     return vals[0]

    # @carbon_source.expression
    # def carbon_source(cls):
    #     PreparationStep = class_registry["PreparationStep"]
    #     return (
    #         select([PreparationStep.carbon_source])
    #         .where(
    #             and_(
    #                 PreparationStep.recipe_id == cls.id,
    #                 PreparationStep.carbon_source != None,
    #             )
    #         )
    #         .correlate(cls)
    #         .limit(1)
    #         .label("carbon_source")
    #     )

    @hybrid_property
    def uses_helium(self):
        return any([p.helium_flow_rate for p in self.preparation_steps])

    @uses_helium.expression
    def uses_helium(cls):
        PreparationStep = class_registry["PreparationStep"]
        s = (
            select([PreparationStep.helium_flow_rate])
            .where(
                and_(
                    PreparationStep.helium_flow_rate != None,
                    PreparationStep.recipe_id == cls.id,
                )
            )
            .correlate(cls)
        )
        return exists(s)

    @hybrid_property
    def uses_argon(self):
        return any([p.argon_flow_rate for p in self.preparation_steps])

    @uses_argon.expression
    def uses_argon(cls):
        PreparationStep = class_registry["PreparationStep"]
        s = (
            select([PreparationStep.argon_flow_rate])
            .where(
                and_(
                    PreparationStep.argon_flow_rate != None,
                    PreparationStep.recipe_id == cls.id,
                )
            )
            .correlate(cls)
        )
        return exists(s)

    @hybrid_property
    def uses_hydrogen(self):
        return any([p.hydrogen_flow_rate for p in self.preparation_steps])

    @uses_hydrogen.expression
    def uses_hydrogen(cls):
        PreparationStep = class_registry["PreparationStep"]
        s = (
            select([PreparationStep.hydrogen_flow_rate])
            .where(
                and_(
                    PreparationStep.hydrogen_flow_rate != None,
                    PreparationStep.recipe_id == cls.id,
                )
            )
            .correlate(cls)
        )
        return exists(s)
