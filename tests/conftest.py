import copy
import os
import json

import pytest  # type: ignore
import responses  # type: ignore
from http import HTTPStatus

from lighthouse import create_app

from .data.fixture_data import (
    CENTRES,
    SAMPLES,
    SAMPLES_DECLARATIONS,
    LOTS_OF_SAMPLES,
    LOTS_OF_SAMPLES_DECLARATIONS_PAYLOAD,
    MULTIPLE_ERRORS_SAMPLES_DECLARATIONS,
    SAMPLES_NO_DECLARATION,
    SAMPLES_FOR_MLWH_UPDATE,
    COG_UK_IDS,
    MLWH_LH_SAMPLES,
    MLWH_LH_SAMPLES_MULTIPLE,
    SAMPLES_CT_VALUES,
    SAMPLES_DIFFERENT_PLATES,
    EVENT_WH_DATA,
    MLWH_SAMPLE_STOCK_RESOURCE
)

from lighthouse.helpers.mysql_db import create_mysql_connection_engine, get_table


@pytest.fixture
def app():
    # set the 'EVE_SETTINGS' env variable to easily switch to the testing environment when creating
    #   an app
    os.environ["EVE_SETTINGS"] = "test.py"

    app = create_app()

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
def empty_data_when_finish(app):
    yield

    with app.app_context():
        mydb = app.data.driver.db
        mydb.samples.delete_many({})
        mydb.samples_declarations.delete_many({})
        mydb.centres.delete_many({})


@pytest.fixture
def samples_declarations(app):
    with app.app_context():
        samples_declarations_collections = app.data.driver.db.samples_declarations
        _ = samples_declarations_collections.insert_many(SAMPLES_DECLARATIONS)

    yield copy.deepcopy(SAMPLES_DECLARATIONS)

    # clear up after the fixture is used
    with app.app_context():
        samples_declarations_collections.delete_many({})


@pytest.fixture
def lots_of_samples_declarations_payload(app):
    yield copy.deepcopy(LOTS_OF_SAMPLES_DECLARATIONS_PAYLOAD)


@pytest.fixture
def multiple_errors_samples_declarations_payload(app):
    yield copy.deepcopy(MULTIPLE_ERRORS_SAMPLES_DECLARATIONS)


@pytest.fixture
def lots_of_samples(app):
    with app.app_context():
        samples_collections = app.data.driver.db.samples
        _ = samples_collections.insert_many(LOTS_OF_SAMPLES)

    yield copy.deepcopy(LOTS_OF_SAMPLES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collections.delete_many({})


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
def samples_different_plates(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES_DIFFERENT_PLATES)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES_DIFFERENT_PLATES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def samples_ct_values(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES_CT_VALUES)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES_CT_VALUES)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def samples_no_declaration(app):
    with app.app_context():
        samples_collection = app.data.driver.db.samples
        _ = samples_collection.insert_many(SAMPLES_NO_DECLARATION)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SAMPLES_NO_DECLARATION)

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def labwhere_samples_simple(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares_by_barcode"

    body = json.dumps([{"barcode": "123", "location_barcode": "4567"}])
    mocked_responses.add(
        responses.POST,
        labwhere_url,
        body=body,
        status=HTTPStatus.OK,
    )


@pytest.fixture
def labwhere_samples_multiple(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares_by_barcode"

    body = json.dumps(
        [
            {"barcode": "123", "location_barcode": "4567"},
            {"barcode": "456", "location_barcode": "1234"},
            {"barcode": "789", "location_barcode": None},
        ]
    )
    mocked_responses.add(
        responses.POST,
        labwhere_url,
        body=body,
        status=HTTPStatus.OK,
    )


@pytest.fixture
def labwhere_samples_error(app, mocked_responses):
    labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/labwares_by_barcode"

    body = json.dumps([])
    mocked_responses.add(
        responses.POST,
        labwhere_url,
        body=body,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

@pytest.fixture
def samples_for_mlwh_update(cog_uk_ids):
    return SAMPLES_FOR_MLWH_UPDATE


@pytest.fixture
def cog_uk_ids():
    return COG_UK_IDS


# ********************** WAREHOUSE DATA ************************** #

@pytest.fixture
def mlwh_lh_samples(app, mlwh_sql_engine):
    insert_into_mlwh(app, MLWH_LH_SAMPLES, mlwh_sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

@pytest.fixture
def mlwh_lh_samples_multiple(app, mlwh_sql_engine):
    insert_into_mlwh(app, MLWH_LH_SAMPLES_MULTIPLE, mlwh_sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

@pytest.fixture
def mlwh_sample_stock_resource(app, mlwh_sql_engine):
    # deletes
    delete_from_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['stock_resource'], mlwh_sql_engine, app.config["MLWH_STOCK_RESOURCES_TABLE"])
    delete_from_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['sample'], mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
    delete_from_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['study'], mlwh_sql_engine, app.config["MLWH_STUDY_TABLE"])

    # inserts
    insert_into_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['sample'], mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
    insert_into_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['study'], mlwh_sql_engine, app.config["MLWH_STUDY_TABLE"])
    insert_into_mlwh(app, MLWH_SAMPLE_STOCK_RESOURCE['stock_resource'], mlwh_sql_engine, app.config["MLWH_STOCK_RESOURCES_TABLE"])

def insert_into_mlwh(app, data, mlwh_sql_engine, table_name):
    table = get_table(mlwh_sql_engine, table_name)

    with mlwh_sql_engine.begin() as connection:
        connection.execute(table.delete())  # delete all rows from table first
        print("Inserting MLWH test data")
        connection.execute(table.insert(), data)

def delete_from_mlwh(app, data, mlwh_sql_engine, table_name):
    table = get_table(mlwh_sql_engine, table_name)

    with mlwh_sql_engine.begin() as connection:
        print("Deleting MLWH test data")
        connection.execute(table.delete())

@pytest.fixture
def event_wh_data(app, event_wh_sql_engine):
    insert_data_into_events_warehouse_tables(app, EVENT_WH_DATA, event_wh_sql_engine)

def insert_data_into_events_warehouse_tables(app, data, event_wh_sql_engine):
    subjects_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_SUBJECTS_TABLE"])
    roles_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_ROLES_TABLE"])
    events_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_EVENTS_TABLE"])
    event_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_EVENT_TYPES_TABLE"])
    subject_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_SUBJECT_TYPES_TABLE"])
    role_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_ROLE_TYPES_TABLE"])

    with event_wh_sql_engine.begin() as connection:
        # delete all rows from each table
        connection.execute(roles_table.delete())
        connection.execute(subjects_table.delete())
        connection.execute(events_table.delete())
        connection.execute(event_types_table.delete())
        connection.execute(subject_types_table.delete())
        connection.execute(role_types_table.delete())

        print("Inserting Events Warehouse test data")
        connection.execute(role_types_table.insert(), data['role_types'])
        connection.execute(event_types_table.insert(), data['event_types'])
        connection.execute(subject_types_table.insert(), data['subject_types'])
        connection.execute(subjects_table.insert(), data['subjects'])
        connection.execute(events_table.insert(), data['events'])
        connection.execute(roles_table.insert(), data['roles'])


@pytest.fixture
def mlwh_sql_engine(app):
    return create_mysql_connection_engine(app.config["WAREHOUSES_RW_CONN_STRING"], app.config["ML_WH_DB"])

@pytest.fixture
def event_wh_sql_engine(app):
    return create_mysql_connection_engine(app.config["WAREHOUSES_RW_CONN_STRING"], app.config["EVENTS_WH_DB"])
