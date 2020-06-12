from http import HTTPStatus
from unittest.mock import patch

import responses
import json

TIMESTAMP = "2013-04-04T10:29:13"


def test_get_empty_samples_declarations(client):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert response.json["_items"] == []


def test_get_samples_declarations_with_content(client, samples_declarations):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["_items"]) == 4


def test_post_new_sample_declaration_for_existing_samples(client, samples_declarations):
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
            ]
        ),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.CREATED, response.json
    assert len(response.json["_items"]) == 2
    assert response.json["_items"][0]["_status"] == "OK"


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


def test_create_lots_of_samples(client, lots_of_samples):

    response = client.post(
        "/samples_declarations", data=json.dumps(lots_of_samples), content_type="application/json",
    )
    assert len(response.json["_items"]) == 1000
    assert response.json["_items"][0]["_status"] == "OK"
