from http import HTTPStatus


def test_priority_samples_validator(app, client):
    with app.app_context():
        rv = client.post(
            "/priority_samples",
            data={"test": True},
            headers={"Authorization": app.config.get("API_TOKENS_PRIORITY").get("read_write")},
        )
        assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
