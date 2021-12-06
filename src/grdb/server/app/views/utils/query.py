from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..experiments import (
    Author, EnvironmentConditions, Experiment, Furnace, Recipe, Substrate, Properties)


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
    if params.get('rcs') or params.get('rbp'):
        q = q.join(Experiment.recipe, isouter=True)
        if params.get('rcs'):  # recipe.carbon_source
            q = q.filter(Recipe.carbon_source == params.get('rcs'))
        if params.get('rbp'):  # recipe.base_pressure
            q = add_inequality_filter(q, Recipe.base_pressure, params.get('rbp'))
    if params.get('sc') or params.get('st') or params.get('sd') or params.get('sl') or params.get('ssa'):
        q = q.join(Experiment.substrate, isouter=True)
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
    if params.get('edp') or params.get('eat'):
        q = q.join(Experiment.environment_conditions, isouter=True)
        if params.get('edp'):  # environment_condition.dew_point
            q = add_inequality_filter(q, EnvironmentConditions.dew_point, params.get('edp'))
        if params.get('eat'):  # environment_condition.ambient_temperature
            q = add_inequality_filter(q, EnvironmentConditions.ambient_temperature, params.get('eat'))
    if params.get('ftd') or params.get('fcsa') or params.get('ftl') or params.get('flhr'):
        q = q.join(Experiment.furnace, isouter=True)
        if params.get('ftd'):  # furnace.tube_diameter
            q = add_inequality_filter(q, Furnace.tube_diameter, params.get('ftd'))
        if params.get('fcsa'):  # furnace.cross_sectional_area
            q = add_inequality_filter(q, Furnace.cross_sectional_area, params.get('fcsa'))
        if params.get('ftl'):  # furnace.tube_length
            q = add_inequality_filter(q, Furnace.tube_length, params.get('ftl'))
        if params.get('flhr'):  # furnace.length_of_heated_region
            q = add_inequality_filter(q, Furnace.length_of_heated_region, params.get('flhr'))
    if params.get('patg') or params.get('psdg') or params.get('pnl') \
            or params.get('pgc') or params.get('pds') or params.get('ps'):
        q = q.join(Experiment.properties, isouter=True)
        if params.get('patg'):  # properties.average_thickness_of_growth
            q = add_inequality_filter(q, Properties.average_thickness_of_growth, params.get('patg'))
        if params.get('psdg'):  # properties.standard_deviation_of_growth
            q = add_inequality_filter(q, Properties.standard_deviation_of_growth, params.get('psdg'))
        if params.get('pnl'):  # properties.number_of_layers
            q = add_inequality_filter(q, Properties.number_of_layers, params.get('pnl'))
        if params.get('pgc'):  # properties.growth_coverage
            q = add_inequality_filter(q, Properties.growth_coverage, params.get('pgc'))
        if params.get('pds'):  # properties.domain_size
            q = add_inequality_filter(q, Properties.domain_size, params.get('pds'))
        if params.get('ps'):  # properties.shape
            q = q.filter(Properties.shape == params.get('ps'))

    return q.all()
