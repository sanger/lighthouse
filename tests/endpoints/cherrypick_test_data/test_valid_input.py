from http import HTTPStatus

from lighthouse.constants.cherrypick_test_data import CPTD_STATUS_PENDING


def test_create_run_successful(client):
    add_to_dart = True
    plate_specs = [[1, 0], [2, 96]]

    post_response = client.post(
        "/cherrypick-test-data",
        json={"add_to_dart": add_to_dart, "plate_specs": plate_specs},
    )

    assert post_response.status_code == HTTPStatus.CREATED

    item_endpoint = post_response.json["_links"]["self"]["href"]
    get_response = client.get(item_endpoint)

    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["status"] == CPTD_STATUS_PENDING
    assert get_response.json["add_to_dart"] == add_to_dart
    assert get_response.json["plate_specs"] == plate_specs
