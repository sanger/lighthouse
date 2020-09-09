import os
import pprint
from logging import Handler, Logger

from slack import WebClient
from slack.errors import SlackApiError

client = WebClient(token=os.getenv("SLACK_API_TOKEN"))


class SlackHandler(Handler):
    def __init__(self, token, channel_id):
        Handler.__init__(self)
        self.client = WebClient(token)
        self.channel_id = channel_id

    def emit(self, record):
        log_entry = self.format(record)
        self.send_message(log_entry)

    def send_message(self, sent_str):
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": sent_str}}],
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")


def pretty(logger: Logger, to_log: object) -> None:
    """Pretty prints the object to ease debugging. Logs at DEBUG and prints object over multiple
    calls to the logger to should not be used in production where exporting logs to logstash at
    per line.

    Arguments:
        logger {Logger} -- the logger to use
        to_log {object} -- object to be pretty printed
    """
    # https://stackoverflow.com/a/21024454
    for line in pprint.pformat(to_log).split("\n"):
        logger.debug(line)
