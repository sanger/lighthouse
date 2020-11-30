from flask import current_app as app


def get_routing_key(event_type: str) -> str:
    """Determines the routing key for a plate event message.

    Arguments:
        event_type {str} -- The event type for which to determine a routing key

    Returns:
        {str} -- The message routing key.
    """
    return app.config["RMQ_ROUTING_KEY"].replace("#", event_type)
