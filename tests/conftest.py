import copy
import os
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
import responses

from lighthouse import create_app
from lighthouse.constants.events import PE_BECKMAN_SOURCE_ALL_NEGATIVES, PE_BECKMAN_SOURCE_COMPLETED
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER,
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME,
    FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER,
    FIELD_CHERRYTRACK_USER_ID,
    FIELD_SAMPLE_ID,
)
from lighthouse.db.dart import load_sql_server_script
from lighthouse.helpers.dart import create_dart_connection
from lighthouse.helpers.mysql import create_mysql_connection_engine, get_table
from lighthouse.messages.message import Message
from lighthouse.types import EventMessage
from tests.fixtures.data.biosero.destination_plate_wells import build_cherrytrack_destination_plate_response
from tests.fixtures.data.biosero.source_plate_wells import build_cherrytrack_source_plates_response
from tests.fixtures.data.centres import CENTRES
from tests.fixtures.data.dart import DART_MONGO_MERGED_SAMPLES
from tests.fixtures.data.event_wh import EVENT_WH_DATA
from tests.fixtures.data.mlwh import (
    COG_UK_IDS,
    MLWH_LH_SAMPLES,
    MLWH_LH_SAMPLES_MULTIPLE,
    MLWH_SAMPLE_LIGHTHOUSE_SAMPLE,
    MLWH_SAMPLE_STOCK_RESOURCE,
    SAMPLES_FOR_MLWH_UPDATE,
    cherrytrack_mlwh_example,
)
from tests.fixtures.data.plate_events import PLATE_EVENTS
from tests.fixtures.data.plates_lookup import PLATES_LOOKUP_WITH_SAMPLES, PLATES_LOOKUP_WITHOUT_SAMPLES
from tests.fixtures.data.positive_samples_in_source_plate import POSITIVE_SAMPLES
from tests.fixtures.data.priority_samples import PRIORITY_SAMPLES
from tests.fixtures.data.samples import SAMPLES, rows_for_samples_in_cherrytrack
from tests.fixtures.data.source_plates import SOURCE_PLATES


@pytest.fixture
def app():
    # set the 'EVE_SETTINGS' env variable to easily switch to the testing environment when creating an app
    os.environ["EVE_SETTINGS"] = "test.py"

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def biosero_auth_headers(app):
    with app.app_context():
        return {"Authorization": app.config.get("API_TOKENS_EVENTS").get("biosero_read_write")}


@pytest.fixture
def lighthouse_ui_auth_headers(app):
    with app.app_context():
        return {"Authorization": app.config.get("API_TOKENS_EVENTS").get("lighthouse_ui_read_write")}


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


@pytest.fixture(params=[SAMPLES])
def samples(app, request):
    samples_to_insert = request.param

    with app.app_context():
        samples_collection = app.data.driver.db.samples
        inserted_samples = samples_collection.insert_many(samples_to_insert)

    #  yield a copy of so that the test change it however it wants
    yield copy.deepcopy(samples_to_insert), inserted_samples

    # clear up after the fixture is used
    with app.app_context():
        samples_collection.delete_many({})


@pytest.fixture
def clear_events(app):
    try:
        yield
    finally:
        with app.app_context():
            events_collection = app.data.driver.db.events
            events_collection.delete_many({})


@pytest.fixture
def priority_samples(app, samples):
    _, samples = samples

    # create a copy so that the test can change it however it needs
    priority_samples = copy.deepcopy(PRIORITY_SAMPLES)

    # update the priority samples with the _id of the samples inserted into mongo, currently only uses the number
    #   of priority samples therefore PRIORITY_SAMPLES needs to be <= SAMPLES
    for count, priority_sample in enumerate(priority_samples):
        priority_sample[FIELD_SAMPLE_ID] = samples.inserted_ids[count]

    with app.app_context():
        priority_samples_collection = app.data.driver.db.priority_samples
        _ = priority_samples_collection.insert_many(priority_samples)

    yield priority_samples

    # clear up after the fixture is used
    with app.app_context():
        priority_samples_collection.delete_many({})


@pytest.fixture
def source_plates(app):
    with app.app_context():
        source_plates_collection = app.data.driver.db.source_plates
        _ = source_plates_collection.insert_many(SOURCE_PLATES)

    #  yield a copy of that the test change it however it wants
    yield copy.deepcopy(SOURCE_PLATES)

    # clear up after the fixture is used
    with app.app_context():
        source_plates_collection.delete_many({})


@pytest.fixture
def positive_samples_in_source_plate(app):
    with app.app_context():
        yield POSITIVE_SAMPLES


@pytest.fixture(scope="function")
def endpoint_url(app, request):
    url = f"/v1/plate-events/create?event_type={request.param}"
    if request.param != "lh_beckman_cp_source_plate_unrecognised":
        url = url + "&barcode=GLS-GP-016240"

    return url


@pytest.fixture
def plate_events(app):
    with app.app_context():
        events_collection = app.data.driver.db.events
        inserted_events = events_collection.insert_many(PLATE_EVENTS)

    #  yield a copy of so that the test change it however it wants
    yield copy.deepcopy(PLATE_EVENTS), inserted_events

    # clear up after the fixture is used
    with app.app_context():
        events_collection.delete_many({})


@pytest.fixture
def mocked_responses():
    """Easily mock responses from HTTP calls.
    https://github.com/getsentry/responses#responses-as-a-pytest-fixture"""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def labwhere_samples_simple(app, mocked_responses):
    labwhere_url = f"{app.config['LABWHERE_URL']}/api/labwares_by_barcode"

    body = [
        {
            "barcode": "plate_123",
            "location_barcode": "location_123",
        }
    ]
    mocked_responses.add(responses.POST, labwhere_url, json=body, status=HTTPStatus.OK)


@pytest.fixture
def samples_for_mlwh_update():
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
def mlwh_sentinel_cherrypicked(app, mlwh_sql_engine):
    def delete_data():
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_STOCK_RESOURCES_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_STUDY_TABLE"])

    try:
        delete_data()

        # inserts
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["sample"],
            mlwh_sql_engine,
            app.config["MLWH_SAMPLE_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["study"],
            mlwh_sql_engine,
            app.config["MLWH_STUDY_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["stock_resource"],
            mlwh_sql_engine,
            app.config["MLWH_STOCK_RESOURCES_TABLE"],
        )

        yield
    finally:
        delete_data()


@pytest.fixture
def mlwh_beckman_cherrypicked(app, mlwh_sql_engine):
    def delete_data():
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

    try:
        delete_data()

        # inserts
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_LIGHTHOUSE_SAMPLE["lighthouse_sample"],
            mlwh_sql_engine,
            app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_LIGHTHOUSE_SAMPLE["sample"],
            mlwh_sql_engine,
            app.config["MLWH_SAMPLE_TABLE"],
        )

        yield
    finally:
        delete_data()


@pytest.fixture
def mlwh_sentinel_and_beckman_cherrypicked(app, mlwh_sql_engine):
    def delete_data():
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_STOCK_RESOURCES_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_STUDY_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

    try:
        delete_data()

        # inserts
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_LIGHTHOUSE_SAMPLE["lighthouse_sample"],
            mlwh_sql_engine,
            app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["sample"] + MLWH_SAMPLE_LIGHTHOUSE_SAMPLE["sample"],  # type: ignore
            mlwh_sql_engine,
            app.config["MLWH_SAMPLE_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["study"],
            mlwh_sql_engine,
            app.config["MLWH_STUDY_TABLE"],
        )
        insert_into_mlwh(
            app,
            MLWH_SAMPLE_STOCK_RESOURCE["stock_resource"],
            mlwh_sql_engine,
            app.config["MLWH_STOCK_RESOURCES_TABLE"],
        )

        yield
    finally:
        delete_data()


def insert_into_mlwh(app, data, mlwh_sql_engine, table_name):
    table = get_table(mlwh_sql_engine, table_name)

    with mlwh_sql_engine.begin() as connection:
        connection.execute(table.delete())  # delete all rows from table first
        print("Inserting MLWH test data")
        connection.execute(table.insert(), data)


def delete_from_mlwh(app, mlwh_sql_engine, table_name):
    table = get_table(mlwh_sql_engine, table_name)

    with mlwh_sql_engine.begin() as connection:
        print("Deleting MLWH test data")
        connection.execute(table.delete())


@pytest.fixture
def event_wh_data(app, event_wh_sql_engine):
    try:
        subjects_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_SUBJECTS_TABLE"])
        roles_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_ROLES_TABLE"])
        events_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_EVENTS_TABLE"])
        event_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_EVENT_TYPES_TABLE"])
        subject_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_SUBJECT_TYPES_TABLE"])
        role_types_table = get_table(event_wh_sql_engine, app.config["EVENT_WH_ROLE_TYPES_TABLE"])

        def delete_event_warehouse_data():
            with event_wh_sql_engine.begin() as connection:
                connection.execute(roles_table.delete())
                connection.execute(subjects_table.delete())
                connection.execute(events_table.delete())
                connection.execute(event_types_table.delete())
                connection.execute(subject_types_table.delete())
                connection.execute(role_types_table.delete())

        delete_event_warehouse_data()

        with event_wh_sql_engine.begin() as connection:
            print("Inserting Events Warehouse test data")
            connection.execute(role_types_table.insert(), EVENT_WH_DATA["role_types"])
            connection.execute(event_types_table.insert(), EVENT_WH_DATA["event_types"])
            connection.execute(subject_types_table.insert(), EVENT_WH_DATA["subject_types"])
            connection.execute(subjects_table.insert(), EVENT_WH_DATA["subjects"])
            connection.execute(events_table.insert(), EVENT_WH_DATA["events"])
            connection.execute(roles_table.insert(), EVENT_WH_DATA["roles"])

        yield
    finally:
        delete_event_warehouse_data()


@pytest.fixture
def mlwh_sql_engine(app):
    return create_mysql_connection_engine(app.config["WAREHOUSES_RW_CONN_STRING"], app.config["MLWH_DB"])


@pytest.fixture
def dart_connection(app):
    return create_dart_connection()


@pytest.fixture
def dart_schema_create(app):
    with app.app_context():
        load_sql_server_script("tests/data/dart/schema.sql")
    yield True
    with app.app_context():
        load_sql_server_script("tests/data/dart/drop_schema.sql")


@pytest.fixture
def dart_samples(app, dart_schema_create):
    with app.app_context():
        load_sql_server_script("tests/data/dart/seed.sql")


@pytest.fixture
def dart_mongo_merged_samples():
    return DART_MONGO_MERGED_SAMPLES


@pytest.fixture
def event_wh_sql_engine(app):
    return create_mysql_connection_engine(app.config["WAREHOUSES_RW_CONN_STRING"], app.config["EVENTS_WH_DB"])


@pytest.fixture
def message_unknown():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": "no_callbacks",
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)


@pytest.fixture
def message_source_complete():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": PE_BECKMAN_SOURCE_COMPLETED,
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [
                {
                    "role_type": "sample",
                    "subject_type": "sample",
                    "friendly_name": "friendly_name",
                    "uuid": "00000000-1111-2222-3333-555555555555",
                },
                {
                    "role_type": "cherrypicking_source_labware",
                    "subject_type": "plate",
                    "friendly_name": "plate-barcode",
                    "uuid": "00000000-1111-2222-3333-555555555556",
                },
                {
                    "role_type": "robot",
                    "subject_type": "robot",
                    "friendly_name": "robot-serial",
                    "uuid": "00000000-1111-2222-3333-555555555557",
                },
            ],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)


@pytest.fixture
def message_source_all_negative():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": PE_BECKMAN_SOURCE_ALL_NEGATIVES,
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [
                {
                    "role_type": "cherrypicking_source_labware",
                    "subject_type": "plate",
                    "friendly_name": "plate-barcode",
                    "uuid": "00000000-1111-2222-3333-555555555556",
                },
                {
                    "role_type": "robot",
                    "subject_type": "robot",
                    "friendly_name": "robot-serial",
                    "uuid": "00000000-1111-2222-3333-555555555557",
                },
            ],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)


@pytest.fixture
def plates_lookup_with_samples(samples, priority_samples):
    return PLATES_LOOKUP_WITH_SAMPLES


@pytest.fixture
def plates_lookup_without_samples(samples, priority_samples):
    return PLATES_LOOKUP_WITHOUT_SAMPLES


@pytest.fixture
def mocked_rabbit_channel(app):
    with app.app_context():
        mocked_broker = MagicMock()
        with patch("lighthouse.classes.services.warehouse.Broker", return_value=mocked_broker):
            mocked_channel = MagicMock()
            mocked_broker.__enter__.return_value = mocked_channel

            yield mocked_channel


@pytest.fixture
def cherrytrack_mock_run_info(
    app, mocked_responses, run_id, cherrytrack_run_info_response, cherrytrack_mock_run_info_status
):
    run_url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

    mocked_responses.add(
        responses.GET,
        run_url,
        json=cherrytrack_run_info_response,
        status=cherrytrack_mock_run_info_status,
    )
    yield


@pytest.fixture
def baracoda_mock_barcodes_group(app, mocked_responses, baracoda_mock_responses, baracoda_mock_status):
    for centre_prefix in baracoda_mock_responses.keys():
        if baracoda_mock_responses[centre_prefix] is not None:
            num_samples = len(baracoda_mock_responses[centre_prefix]["barcodes_group"]["barcodes"])
            baracoda_url = f"{app.config['BARACODA_URL']}" f"/barcodes_group/{centre_prefix}/new?count={num_samples}"
            mocked_responses.add(
                responses.POST,
                baracoda_url,
                json=baracoda_mock_responses[centre_prefix],
                status=baracoda_mock_status,
            )
    yield


@pytest.fixture
def cherrytrack_mock_source_plates_status():
    return HTTPStatus.OK


@pytest.fixture
def cherrytrack_mock_run_info_status():
    return HTTPStatus.OK


@pytest.fixture
def cherrytrack_mock_destination_plate_status():
    return HTTPStatus.OK


@pytest.fixture
def baracoda_mock_status():
    return HTTPStatus.CREATED


@pytest.fixture
def cherrytrack_mock_source_plates(
    app,
    mocked_responses,
    source_barcode,
    destination_barcode,
    cherrytrack_source_plates_response,
    cherrytrack_mock_source_plates_status,
):
    source_plates_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_barcode}"
    mocked_responses.add(
        responses.GET,
        source_plates_url,
        json=cherrytrack_source_plates_response,
        status=cherrytrack_mock_source_plates_status,
    )
    yield


@pytest.fixture
def cherrytrack_mock_destination_plate(
    app,
    mocked_responses,
    destination_barcode,
    cherrytrack_destination_plate_response,
    cherrytrack_mock_destination_plate_status,
):
    destination_plate_url = f"{app.config['CHERRYTRACK_URL']}/destination-plates/{destination_barcode}"
    mocked_responses.add(
        responses.GET,
        destination_plate_url,
        json=cherrytrack_destination_plate_response,
        status=cherrytrack_mock_destination_plate_status,
    )
    yield


@pytest.fixture
def cherrytrack_run_info_response(run_id):
    return {
        "data": {
            "id": run_id,
            FIELD_CHERRYTRACK_USER_ID: "user1",
            FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "aLiquidHandlerSerialNumber",
            FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
            FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: "CPA",
        }
    }


@pytest.fixture
def cherrytrack_destination_plate_response(destination_barcode, source_barcode, run_id):
    return build_cherrytrack_destination_plate_response(destination_barcode, source_barcode, run_id)


def cherrytrack_destination_plate_response_duplicated_wells(cherrytrack_destination_plate_response):
    cherrytrack_destination_plate_response["wells"][0]["destination_coordinate"] = "H12"
    return cherrytrack_destination_plate_response


@pytest.fixture
def cherrytrack_source_plates_response(run_id, source_barcode, destination_barcode):
    return build_cherrytrack_source_plates_response(run_id, source_barcode, destination_barcode)


@pytest.fixture
def samples_from_cherrytrack_into_mongo(app, source_barcode):
    try:
        samples = rows_for_samples_in_cherrytrack(source_barcode)

        with app.app_context():
            samples_collection = app.data.driver.db.samples
            inserted_samples = samples_collection.insert_many(samples)

        #  yield a copy of so that the test change it however it wants
        yield copy.deepcopy(samples), inserted_samples

    # clear up after the fixture is used
    finally:
        samples_collection.delete_many({})


@pytest.fixture
def mlwh_samples_in_cherrytrack(app, source_barcode, mlwh_sql_engine):
    def delete_data():
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_SAMPLE_TABLE"])
        delete_from_mlwh(app, mlwh_sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

    try:
        delete_data()

        example = cherrytrack_mlwh_example(source_barcode)

        # inserts
        insert_into_mlwh(
            app,
            example["lighthouse_sample"],
            mlwh_sql_engine,
            app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"],
        )
        insert_into_mlwh(
            app,
            example["sample"],
            mlwh_sql_engine,
            app.config["MLWH_SAMPLE_TABLE"],
        )

        yield
    finally:
        delete_data()
