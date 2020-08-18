from http import HTTPStatus


def test_create_report(client, samples, samples_declarations, labwhere_samples_simple):
    response = client.post("/reports/new", content_type="application/json",)
    assert response.status_code == HTTPStatus.CREATED
