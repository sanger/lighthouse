from http import HTTPStatus
from unittest.mock import patch

import responses
import json
from tests.data.fixture_data import LOTS_OF_SAMPLES_DECLARATIONS

TIMESTAMP = "2013-04-04T10:29:13"


def test_get_empty_samples_declarations(client):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert response.json["_items"] == []


def test_get_samples_declarations_with_content(client, samples_declarations):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["_items"]) == 4


def test_post_new_sample_declaration_for_existing_samples_unauthorized(
    client, samples_declarations
):
    response = client.post(
        "/samples_declarations",
        data=json.dumps(
            [
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
            ],
        ),
        content_type="application/json",
        headers={"LIGHTHOUSE_API_KEY": "wronk key!!!"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.json


def post_authorized_create_samples_declaration(client, payload):
    return client.post(
        "/samples_declarations",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"LIGHTHOUSE_API_KEY": "develop"},
    )


def test_post_new_sample_declaration_for_existing_samples(client, samples, samples_declarations):
    items = [
            {"root_sample_id": "MCM001", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
            {"root_sample_id": "MCM003", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
        ],
    response = post_authorized_create_samples_declaration(
        client,
        items
    )
    assert response.status_code == HTTPStatus.CREATED, response.json
    assert response.json["_status"] == "OK"
    assert len(response.json["_items"]) == 2
    assert response.json["_items"][0]["_status"] == "OK"

    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert response.json["_items"] == items

def test_create_lots_of_samples(client, lots_of_samples):
    response = post_authorized_create_samples_declaration(client, LOTS_OF_SAMPLES_DECLARATIONS)
    assert len(response.json["_items"]) == 100000
    assert response.json["_status"] == "OK"
    assert response.json["_items"][0]["_status"] == "OK"


def test_wrong_value_for_value_in_sequencing(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [
            {
                "root_sample_id": "MCM001",
                "value_in_sequencing": "wrong answer!!",
                "declared_at": TIMESTAMP,
            },
            {   "root_sample_id": "MCM003", 
                "value_in_sequencing": "Yes", 
                "declared_at": TIMESTAMP,
            },
        ],
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "ERR"
    assert response.json["_items"][0]["_issues"] == {
        "value_in_sequencing": "unallowed value wrong answer!!"
    }
    assert response.json["_items"][1]["_status"] == "OK"


def test_wrong_value_for_declared_at(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [
            {
                "root_sample_id": "MCM001",
                "value_in_sequencing": "Unknown",
                "declared_at": TIMESTAMP,
            },
            {
                "root_sample_id": "MCM003",
                "value_in_sequencing": "Yes",
                "declared_at": "wrong time mate!!",
            },
        ],
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "OK"
    assert response.json["_items"][1]["_status"] == "ERR"
    assert response.json["_items"][1]["_issues"] == {"declared_at": "must be of datetime type"}


def test_wrong_value_for_root_sample_id(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [
            {"root_sample_id": True, "value_in_sequencing": "Unknown", "declared_at": TIMESTAMP,},
            {"root_sample_id": "MCM003", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
        ],
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "ERR"
    assert response.json["_items"][0]["_issues"] == {"root_sample_id": "must be of string type"}
    assert response.json["_items"][1]["_status"] == "OK"


def test_validate_sample_exist_in_samples_table(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [
            {
                "root_sample_id": "MCM001",
                "value_in_sequencing": "Unknown",
                "declared_at": TIMESTAMP,
            },
            {
                "root_sample_id": "MCM_WRONG_VALUE",
                "value_in_sequencing": "Yes",
                "declared_at": TIMESTAMP,
            },
        ],
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "OK"
    assert response.json["_items"][1]["_status"] == "ERR"
    # TODO: check error message

def test_validate_sample_not_defined_twice_v1(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [
            {
                "root_sample_id": "MCM001",
                "value_in_sequencing": "Unknown",
                "declared_at": TIMESTAMP,
            },
            {   "root_sample_id": "MCM001", 
                "value_in_sequencing": "Yes", 
                "declared_at": TIMESTAMP,
            },
        ],
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "ERR"
    assert response.json["_items"][1]["_status"] == "ERR"
    # TODO: check error message

def test_validate_sample_not_defined_twice_v2(client, samples, samples_declarations):
    response = post_authorized_create_samples_declaration(
        client,
        [{"root_sample_id": "MCM001", "value_in_sequencing": "Unknown", "declared_at": "2013-04-04T10:29:13"}, 
        {"root_sample_id": "MCM002", "value_in_sequencing": "Unknown", "declared_at": "2013-04-04T10:29:13"}, 
        {"root_sample_id": "MCM001", "value_in_sequencing": "Unknown", "declared_at": "2013-04-04T10:29:13"}, 
        {"root_sample_id": "MCM003", "value_in_sequencing": "Unknown", "declared_at": "2013-04-04T10:29:13"}, 
        {"root_sample_id": "MCM003", "value_in_sequencing": "Unknown", "declared_at": "2013-04-04T10:29:13"}]
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
    assert len(response.json["_items"]) == 5
    assert response.json["_status"] == "ERR"
    assert response.json["_items"][0]["_status"] == "ERR"
    assert response.json["_items"][1]["_status"] == "OK"
    assert response.json["_items"][2]["_status"] == "ERR"
    assert response.json["_items"][3]["_status"] == "ERR"
    assert response.json["_items"][4]["_status"] == "ERR"
    # TODO: check error message

def test_filter_by_root_sample_id(client, samples_declarations):
    response = client.get(
        '/samples_declarations?where={"root_sample_id":"MCM001"}', content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK, response.json
    assert len(response.json["_items"]) == 1, response.json

    assert response.json["_items"][0]["value_in_sequencing"] == "Yes", response.json


def test_get_last_samples_declaration_for_a_root_sample_id(client, samples_declarations):
    response = client.get(
        '/samples_declarations?where={"root_sample_id":"MCM003"}&sort=-declared_at&max_results=1',
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.OK, response.json
    assert len(response.json["_items"]) == 1, response.json

    assert response.json["_items"][0]["value_in_sequencing"] == "Yes", response.json
    assert response.json["_items"][0]["declared_at"] == "2013-04-06T10:29:13", response.json
