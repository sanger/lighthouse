import copy

import pytest  # type: ignore
import responses  # type: ignore

from lighthouse import create_app

from .data.fixture_data import CENTRES, SAMPLES


@pytest.fixture
def app():
    app = create_app(test_config_path="config/test.py")

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def centres(app):
    with app.app_context():
        centres_collection = app.data.driver.db.centres
        _ = centres_collection.insert_many(CENTRES)

    #  yield a copy so that the test change it however it wants
    yield copy.deepcopy(CENTRES)

    # clear up after the fixture is used
    with app.app_context():
        centres_collection.delete_many({})


@pytest.fixture
def samples(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
