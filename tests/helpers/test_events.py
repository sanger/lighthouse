from lighthouse.helpers.events import get_routing_key


# ---------- get_routing_key tests ----------


def test_get_routing_key(app):
    with app.app_context():
        test_event_type = "test_event_type"
        result = get_routing_key(test_event_type)

        assert result == f"test.event.{test_event_type}"
