from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from grdb.database import Base
from grdb.database.models.author import ExperimentToAuthorAssociation

class Experiment(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    __tablename__ = 'experiment'
    __table_args__ = {'extend_existing': True}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement="ignore_fk",
        info={"verbose_name": "ID"},
    )

    # The recipe can be the same for multiple different experiments
    recipe_id = Column(
        Integer,
        ForeignKey("recipe.id", ondelete="CASCADE"),
        info={"verbose_name": "Recipe ID"},
        index=True,
    )
    # REMOVE NEXT FEW LINES - ENV CONDITIONS ARE ONE TO ONE NOT MANY TO ONE
    # The environment conditions can be the same for multiple different experiments
    environment_conditions_id = Column(
        Integer,
        ForeignKey("environment_conditions.id", ondelete="CASCADE"),
        info={"verbose_name": "Environment Conditions ID"},
        index=True,
    )
    # The substrate can be the same for multiple different experiments
    substrate_id = Column(
        Integer,
        ForeignKey("substrate.id", ondelete="CASCADE"),
        info={"verbose_name": "Substrate ID"},
        index=True,
    )
    # The furnace can be the same for multiple different experiments
    furnace_id = Column(
        Integer,
        ForeignKey("furnace.id", ondelete="CASCADE"),
        info={"verbose_name": "Furnace ID"},
        index=True,
    )
    ## The name of the analysis software
    # software_name = Column(String(20), info={"verbose_name": "Analysis Software"})
    ## The version of the analysis software
    # software_version = Column(String(20), info={"verbose_name": "Software Version"})

    # The primary SEM file associated with this experiment
    primary_sem_file_id = Column(Integer, info={"verbose_name": "SEM File ID"}, index=True)

    # The user/author that submitted this experiment
    submitted_by = Column(Integer, ForeignKey('author.id'), info={"verbose_name": "Submitted By"})

    # The date the experiment was conducted
    experiment_date = Column(
        Date, info={"verbose_name": "Experiment Date", "required": True}
    )

    # The material grown
    material_name = Column(
        String(32),
        info={
            "verbose_name": "Material Name",
            "choices": ["Graphene", "other"],
            "required": True,
        },
    )

    # Status of experiment valdation
    validated = Column(Boolean, info={"verbose_name": "Validated"}, default=False)

    # The authors that conducted the experiment
    authors = relationship("Author", secondary="EXP_TO_ATHR_ASSCTN", back_populates="authored_experiments")

    # Just an experiment for a author related hybrid property. Comment if it's a source of problems.
    @hybrid_property
    def authors_string(self):
        return [a.author_last_names for a in self.authors]

    # MANY-TO-ONE: experiments->recipe
    recipe = relationship("Recipe", back_populates="experiments")

    # MANY-TO-ONE: experiments->environment_conditions
    environment_conditions = relationship("EnvironmentConditions", back_populates="experiments")

    # MANY-TO-ONE: experiments->substrate
    substrate = relationship("Substrate", back_populates="experiments")

    # MANY-TO-ONE: experiments->furnace
    furnace = relationship("Furnace", back_populates="experiments")

    # ONE-TO-ONE: experiment -> properties
    properties = relationship(
        "Properties",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="experiment",
        lazy="subquery",
    )

    # ONE-TO-MANY: experiment -> raman_files
    raman_files = relationship(
        "RamanFile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="experiment",
        lazy="subquery",
    )

    # raman_analysis = relationship(
    #     "RamanAnalysis",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    #     passive_deletes=True,
    #     back_populates="experiment",
    #     lazy="subquery",
    # )
    
    # ONE-TO-MANY: experiment -> sem_files
    sem_files = relationship(
        "SemFile",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
        foreign_keys="SemFile.experiment_id",
        back_populates="experiment",
        lazy="subquery",
    )

    # Defining the foreign key constraint explicitly (as below) prevents a sem_file id from
    # a different experiment from being assigned to the primary_sem_file_id column.
    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "primary_sem_file_id"],
            ["sem_file.experiment_id", "sem_file.id"],
            use_alter=True,
            ondelete="CASCADE",
            name="fk_primary_sem_file",
        ),
        # ForeignKeyConstraint(
        #     [software_name, software_version],
        #     ["software.name", "software.version"],
        #     name="fk_gresq_software",
        # ),
    )

    primary_sem_file = relationship(
        "SemFile",
        primaryjoin="Experiment.primary_sem_file_id==SemFile.id",
        foreign_keys=primary_sem_file_id,
        uselist=False,
        post_update=True,
        lazy="subquery",
    )

    @hybrid_property
    def primary_sem_analysis(self):
        return self.primary_sem_file.default_analysis

    # @hybrid_property
    # def author_last_names(self):
    #     return ", ".join(sorted([a.last_name for a in self.authors if a.last_name]))

    def json_encodable(self):
        return {
            "id": self.id,
            "material_name": self.material_name,
            "experiment_date": self.experiment_date.timetuple() if self.experiment_date else None,
            "authors": [s.json_encodable() if s else None for s in self.authors],
            "recipe": self.recipe.json_encodable() if self.recipe else None,
            "properties": self.properties.json_encodable() if self.properties else None,
            "furnace": self.furnace.json_encodable() if self.furnace else None,
            "substrate": self.substrate.json_encodable() if self.substrate else None,
            "environment_conditions": self.environment_conditions.json_encodable() if self.environment_conditions else None,
            "validated": self.validated
        }
