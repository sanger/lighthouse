from lighthouse.helpers import get_samples


def test_samples(client):
    response = client.get("/hello")
    assert response.data == b"hello world"
