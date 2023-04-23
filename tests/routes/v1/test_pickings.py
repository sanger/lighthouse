from http import HTTPStatus
from unittest.mock import patch

import pytest
import responses

ENDPOINT_PREFIXES = ["", "/v1"]
GET_PICKINGS_ENDPOINT = "/pickings"

GET_PICKINGS_ENDPOINTS = [prefix + GET_PICKINGS_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_success(app, client, mocked_responses, endpoint, pickings_plate):
    barcode = "ABCD-1234"
    ss_url = (
        f"{app.config['SS_URL']}/api/v2/labware?filter[barcode]={barcode}&include=purpose,receptacles.aliquots.sample"
    )

    body = pickings_plate

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    response = client.post(endpoint, json={"user": "user1", "robot": "robot1", "barcode": barcode})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"barcode": barcode, "positive_control": "A1", "negative_control": "B1"}


# TODO (DPL-572):
# Test failures:
# missing post data (either: user, robot or barcode)
# stub SS response so that SS is unaccessible
# stub SS response so that no data is returned
# stub SS response so that purpose is incorrect
# stub SS reponse so that data has no samples
# stub SS reponse so that data has missing +ve control
# stub SS reponse so that data has missing -ve control
# stub SS reponse so that data has more than one +ve or -ve control
