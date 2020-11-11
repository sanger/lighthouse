from http import HTTPStatus
from unittest.mock import patch
import pandas as pd

from lighthouse.constants import (
    FIELD_ROOT_SAMPLE_ID
)

def test_create_report(client, samples, samples_declarations, labwhere_samples_simple):
    with patch(
        "lighthouse.helpers.reports.get_cherrypicked_samples",
        return_value=pd.DataFrame(['MCM001'], columns=[FIELD_ROOT_SAMPLE_ID])
    ):
        response = client.post("/reports/new", content_type="application/json",)
        assert response.status_code == HTTPStatus.CREATED
