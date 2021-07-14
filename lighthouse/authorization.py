from eve.auth import TokenAuth
from flask import current_app


class PriorityAPITokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return token in current_app.config["API_TOKENS_PRIORITY"].values()


class EventsAPITokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return token in current_app.config["API_TOKENS_EVENTS"].values()
