from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..index import (
    Author, EnvironmentConditions, Experiment, Furnace, Recipe, Substrate)


def add_inequality_filter(q: Query, column: InstrumentedAttribute, expr: str):
    """ Adds an filter of an inequality statement to the given column by the given query parameter

    Args:
        q (sqlalchemy.orm.Query): Query object to add the filter to
        column (sqlalchemy.orm.attributes.InstrumentedAttribute): Column used for the filter
        expr (str): Inequality expression (ex. lt 10)

    Returns: Filtered Query with q.filter(<column> <inequality> <value>)
                ex) q.filter(Experiment.id == 1)

    """
    inequality = expr[:2].lower()
    value = float(expr[2:])

    if inequality == 'eq':
        q = q.filter(column == value)
    elif inequality == 'ne':
        q = q.filter(column != value)
    elif inequality == 'lt':
        q = q.filter(column < value)
    elif inequality == 'le':
        q = q.filter(column <= value)
    elif inequality == 'gt':
        q = q.filter(column > value)
    elif inequality == 'ge':
        q = q.filter(column >= value)
    return q


def query_experiment_data(q: Query, params: dict) -> list:
    """ A utility function that helps dynamic querying of experiment data based on params.
        If a filtering is done by an equality statement,
        first two characters must be one of the inequality code.

    Args:
        q (sqlalchemy.orm.Query): Must be query of Experiment

        params (dict): A dictionary containing query string info passed into
            /data/experiments endpoint

    Returns: a list of Models remaining after all the filtering.

    """

    q = q.join(Experiment.recipe) \
        .join(Experiment.substrate) \
        .join(Experiment.furnace)

    if params.get('rcs'):  # recipe.carbon_source
        q = q.filter(Recipe.carbon_source == params.get('rcs'))
    if params.get('rbp'):  # recipe.base_pressure
        q = add_inequality_filter(q, Recipe.base_pressure, params.get('rbp'))
    if params.get('sc'):  # substrate.catalyst
        q = q.filter(Substrate.catalyst == params.get('sc'))
    if params.get('st'):  # substrate.thickness
        q = add_inequality_filter(q, Substrate.thickness, params.get('st'))
    if params.get('sd'):  # substrate.diameter
        q = add_inequality_filter(q, Substrate.diameter, params.get('sd'))
    if params.get('sl'):  # substrate.length
        q = add_inequality_filter(q, Substrate.length, params.get('sl'))
    if params.get('ssa'):  # substrate.surface_area
        q = add_inequality_filter(q, Substrate.surface_area, params.get('ssa'))
    if params.get('ftd'):  # furnace.tube_diameter
        q = add_inequality_filter(q, Furnace.tube_diameter, params.get('ftd'))
    if params.get('fcsa'):  # furnace.cross_sectional_area
        q = add_inequality_filter(q, Furnace.cross_sectional_area, params.get('fcsa'))
    if params.get('ftl'):  # furnace.tube_length
        q = add_inequality_filter(q, Furnace.tube_length, params.get('ftl'))
    if params.get('flhr'):  # furnace.length_of_heated_region
        q = add_inequality_filter(q, Furnace.length_of_heated_region, params.get('flhr'))

    return q.all()
