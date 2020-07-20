from http import HTTPStatus
from unittest.mock import patch
import json
import responses  # type: ignore

def test_post_plates_endpoint(app, client, samples, mocked_responses):
    with patch(
      "lighthouse.blueprints.plates.add_cog_barcodes", return_value="TS1",
    ):
      ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

      body = json.dumps({"barcode": "123"})
      mocked_responses.add(
          responses.POST, ss_url, body=body, status=HTTPStatus.OK,
      )

      response = client.post(
        "/plates/new",
        data=json.dumps(
            { "barcode": "123" }
        ),
        content_type="application/json",

      )
      assert response.status_code == HTTPStatus.OK
      assert response.json == { "data": { "plate_barcode": "123", "centre": "TS1", "number_of_positives": 1} }