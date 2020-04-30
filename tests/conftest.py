import pytest
import responses

from lighthouse import create_app

TEST_SETTINGS = {
    "ALLOW_UNKNOWN": True,
    "HATEOAS": True,
    "DOMAIN": {"samples": {}, "imports": {}, "centres": {}, "schema": {}},
    "DEBUG": True,
    # Let's just use the local mongod instance. Edit as needed.
    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    "MONGO_HOST": "127.0.0.1",
    "MONGO_PORT": 27017,
    # Skip this block if your db has no auth. But it really should.
    # MONGO_USERNAME = '<your username>'
    # MONGO_PASSWORD = '<your password>'
    # Name of the database on which the user can be authenticated,
    # needed if --auth mode is enabled.
    # MONGO_AUTH_SOURCE = '<dbname>'
    "MONGO_DBNAME": "lighthouseTestDB",
    "MONGO_QUERY_BLACKLIST": ["$where"],
}


@pytest.fixture
def app():
    TEST_CONFIG = {"TESTING": True, "BARACODA_HOST": "127.0.0.1", "BARACODA_PORT": 5001}

    app = create_app(test_config=TEST_CONFIG, test_settings=TEST_SETTINGS)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def centres(app):
    centres = [
        {"name": "test1", "prefix": "TS1"},
        {"name": "test2", "prefix": "TS2"},
        {"name": "test3", "prefix": "TS3"},
    ]

    with app.app_context():
        centres_collection = app.data.driver.db["centres"]
        _ = centres_collection.insert_many(centres)

    yield centres

    with app.app_context():
        centres_collection.delete_many({})


@pytest.fixture
def samples(app):
    samples = [
        {
            "coordinate": "A01",
            "source": "test1",
            "phenotype": "A phenotype",
            "plate_barcode": "123",
        },
        {
            "coordinate": "B01",
            "source": "test1",
            "phenotype": "A phenotype",
            "plate_barcode": "123",
        },
    ]
    with app.app_context():
        samples_collection = app.data.driver.db["samples"]
        _ = samples_collection.insert_many(samples)

    yield samples

    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
