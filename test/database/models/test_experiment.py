from grdb.database.models import Experiment

def test_experiments_exist(grdb,session):
    experiments = session.query(Experiment).all()
    assert len(experiments) != 0

def test_experiment_has_recipe(grdb,session):
    experiment = session.query(Experiment).first()
    assert experiment.recipe is not None

def test_experiment_has_environment_conditions(grdb,session):
    experiment = session.query(Experiment).first()
    assert experiment.environment_conditions is not None

def test_experiment_has_substrate(grdb,session):
    experiment = session.query(Experiment).first()
    assert experiment.substrate is not None

def test_experiment_has_furnace(grdb,session):
    experiment = session.query(Experiment).first()
    assert experiment.furnace is not None

def test_experiment_has_authors(grdb,session):
    experiment = session.query(Experiment).first()
    print(experiment.authors[0])
    assert len(experiment.authors) != 0

def test_experiment_has_properties(grdb,session):
    experiment = session.query(Experiment).first()
    # print(experiment)
    # print(session.is_active)
    # print(experiment.properties.id)
    # print(experiment.properties.number_of_layers)
    assert experiment.properties != None

def test_experiment_has_raman_files(grdb,session):
    experiment = session.query(Experiment).first()
    assert len(experiment.raman_files) != 0

def test_experiment_has_sem_files(grdb,session):
    experiment = session.query(Experiment).first()
    assert len(experiment.sem_files) != 0