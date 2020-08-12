from http import HTTPStatus
import json

TIMESTAMP = "2013-04-04T10:29:13"


class CheckNumInstancesChangeBy:
    def __init__(self, app, model_name, num):
        with app.app_context():
            self.__num = num
            self.__model_name = model_name
            self.__model = app.data.driver.db[model_name]
            self.__app = app

    def __enter__(self):
        with self.__app.app_context():
            self.__size = self.__model.count()

    def __exit__(self, type, value, tb):
        with self.__app.app_context():
            assert self.__model.count() == self.__size + self.__num


def assert_has_error(record, key, error_message):
    assert record["_status"] == "ERR"
    assert record["_issues"][key] == error_message


def test_get_empty_samples_declarations(client):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert response.json["_items"] == []


def test_get_samples_declarations_with_content(client, samples_declarations):
    response = client.get("/samples_declarations")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["_items"]) == 4


def test_post_new_sample_declaration_for_existing_samples_unauthorized(
    app, client, samples_declarations
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 0):
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
            headers={"x-lighthouse-client": "wronk key!!!"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.json


def post_authorized_create_samples_declaration(client, payload):
    return client.post(
        "/samples_declarations",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"x-lighthouse-client": "develop"},
    )


def test_post_new_single_sample_declaration_for_existing_sample(
    app, client, samples, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        items = {
            "root_sample_id": "MCM001",
            "value_in_sequencing": "Yes",
            "declared_at": TIMESTAMP,
        }

        response = post_authorized_create_samples_declaration(client, items)
        assert response.status_code == HTTPStatus.CREATED, response.json
        assert response.json["_status"] == "OK"


def test_post_new_sample_declaration_for_existing_samples(
    app, client, samples, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 2):
        items = [
            {"root_sample_id": "MCM001", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
            {"root_sample_id": "MCM003", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
        ]

        response = post_authorized_create_samples_declaration(client, items)
        assert response.status_code == HTTPStatus.CREATED, response.json
        assert response.json["_status"] == "OK"
        assert len(response.json["_items"]) == 2
        assert response.json["_items"][0]["_status"] == "OK"
        assert response.json["_items"][1]["_status"] == "OK"


def test_create_lots_of_samples_declarations(
    app, client, lots_of_samples, lots_of_samples_declarations_payload, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(
        app, "samples_declarations", len(lots_of_samples_declarations_payload)
    ):
        response = post_authorized_create_samples_declaration(
            client, lots_of_samples_declarations_payload
        )
        assert len(response.json["_items"]) == len(lots_of_samples_declarations_payload)
        assert response.json["_status"] == "OK"

        for item in response.json["_items"]:
            assert item["_status"] == "OK"


def test_inserts_new_declarations_even_when_other_declarations_are_wrong(
    app, client, samples, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        stamp = "2013-04-10T09:00:00"
        post_authorized_create_samples_declaration(
            client,
            [
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "wrong answer!!",
                    "declared_at": stamp,
                },
                {"root_sample_id": "MCM002", "value_in_sequencing": "Yes", "declared_at": stamp},
            ],
        )
        with app.app_context():
            li = [
                x
                for x in app.data.driver.db.samples_declarations.find({"root_sample_id": "MCM002"})
            ]
            assert len(li) == 1


def test_wrong_value_for_value_in_sequencing(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        response = post_authorized_create_samples_declaration(
            client,
            [
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "wrong answer!!",
                    "declared_at": TIMESTAMP,
                },
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
            ],
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 2
        assert response.json["_status"] == "ERR"
        assert_has_error(
            response.json["_items"][0], "value_in_sequencing", "unallowed value wrong answer!!"
        )
        assert response.json["_items"][1]["_status"] == "OK"


def test_wrong_value_for_declared_at(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
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
        assert_has_error(response.json["_items"][1], "declared_at", "must be of datetime type")


def test_wrong_value_for_root_sample_id(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        response = post_authorized_create_samples_declaration(
            client,
            [
                {
                    "root_sample_id": True,
                    "value_in_sequencing": "Unknown",
                    "declared_at": TIMESTAMP,
                },
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
            ],
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 2
        assert response.json["_status"] == "ERR"
        assert_has_error(response.json["_items"][0], "root_sample_id", "must be of string type")
        assert response.json["_items"][1]["_status"] == "OK"


def test_unknown_sample_for_root_sample_id(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 0):
        response = post_authorized_create_samples_declaration(
            client,
            {"root_sample_id": "nonsense", "value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert response.json["_status"] == "ERR"
        assert_has_error(
            response.json, "root_sample_id", "Sample does not exist in database: nonsense"
        )


def test_missing_value_for_root_sample_id_multiple(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        response = post_authorized_create_samples_declaration(
            client,
            [
                {"value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
            ],
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 2
        assert response.json["_status"] == "ERR"
        assert_has_error(response.json["_items"][0], "root_sample_id", "required field")
        assert response.json["_items"][1]["_status"] == "OK"


def test_missing_value_for_root_sample_id_single(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 0):
        response = post_authorized_create_samples_declaration(
            client, {"value_in_sequencing": "Yes", "declared_at": TIMESTAMP,},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert response.json["_status"] == "ERR"
        assert_has_error(response.json, "root_sample_id", "required field")


def test_validate_sample_exist_in_samples_table(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
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
        assert response.json["_status"] == "ERR"
        assert len(response.json["_items"]) == 2
        assert response.json["_items"][0]["_status"] == "OK"
        assert_has_error(
            response.json["_items"][1],
            "root_sample_id",
            "Sample does not exist in database: MCM_WRONG_VALUE",
        )


def test_validate_samples_are_defined_twice_v1(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 0):
        response = post_authorized_create_samples_declaration(
            client,
            [
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "Unknown",
                    "declared_at": TIMESTAMP,
                },
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "Yes",
                    "declared_at": TIMESTAMP,
                },
            ],
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 2
        assert response.json["_status"] == "ERR"
        assert_has_error(
            response.json["_items"][0], "root_sample_id", "Sample is a duplicate: MCM001"
        )
        assert_has_error(
            response.json["_items"][1], "root_sample_id", "Sample is a duplicate: MCM001"
        )


def test_validate_samples_are_defined_twice_v2(
    app, client, samples, samples_declarations, empty_data_when_finish
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 1):
        response = post_authorized_create_samples_declaration(
            client,
            [
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "Unknown",
                    "declared_at": "2013-04-04T10:29:13",
                },
                {
                    "root_sample_id": "MCM002",
                    "value_in_sequencing": "Unknown",
                    "declared_at": "2013-04-04T10:29:13",
                },
                {
                    "root_sample_id": "MCM001",
                    "value_in_sequencing": "Unknown",
                    "declared_at": "2013-04-04T10:29:13",
                },
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Unknown",
                    "declared_at": "2013-04-04T10:29:13",
                },
                {
                    "root_sample_id": "MCM003",
                    "value_in_sequencing": "Unknown",
                    "declared_at": "2013-04-04T10:29:13",
                },
            ],
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 5
        assert response.json["_status"] == "ERR"
        assert_has_error(
            response.json["_items"][0], "root_sample_id", "Sample is a duplicate: MCM001"
        )
        assert response.json["_items"][1]["_status"] == "OK"
        assert_has_error(
            response.json["_items"][2], "root_sample_id", "Sample is a duplicate: MCM001"
        )
        assert_has_error(
            response.json["_items"][3], "root_sample_id", "Sample is a duplicate: MCM003"
        )
        assert_has_error(
            response.json["_items"][4], "root_sample_id", "Sample is a duplicate: MCM003"
        )


def test_multiple_errors_on_samples_declaration(
    app, client, multiple_errors_samples_declarations_payload
):
    with CheckNumInstancesChangeBy(app, "samples_declarations", 0):
        response = post_authorized_create_samples_declaration(
            client, multiple_errors_samples_declarations_payload
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.json
        assert len(response.json["_items"]) == 8
        assert response.json["_status"] == "ERR"
        assert_has_error(
            response.json["_items"][0],
            "root_sample_id",
            "Sample does not exist in database: YOR10020466",
        )
        assert_has_error(response.json["_items"][1], "root_sample_id", "required field")
        assert_has_error(
            response.json["_items"][2],
            "root_sample_id",
            [
                "Sample does not exist in database: YOR10020379",
                "Sample is a duplicate: YOR10020379",
            ],
        )
        assert_has_error(response.json["_items"][2], "declared_at", "must be of datetime type")
        assert_has_error(
            response.json["_items"][3],
            "root_sample_id",
            "Sample does not exist in database: YOR10020240",
        )
        assert_has_error(
            response.json["_items"][4],
            "root_sample_id",
            [
                "Sample does not exist in database: YOR10020379",
                "Sample is a duplicate: YOR10020379",
            ],
        )
        assert_has_error(
            response.json["_items"][5],
            "root_sample_id",
            "Sample does not exist in database: YOR10020224",
        )
        assert_has_error(
            response.json["_items"][6],
            "root_sample_id",
            "Sample does not exist in database: YOR10020217",
        )
        assert_has_error(response.json["_items"][6], "value_in_sequencing", "required field")
        assert_has_error(
            response.json["_items"][7], "value_in_sequencing", "unallowed value maybelater"
        )


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
