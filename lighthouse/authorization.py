from eve.auth import TokenAuth
from flask import current_app


class APITokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return token == current_app.config["API_TOKEN"]
