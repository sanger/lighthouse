from flask import request, current_app
from eve.auth import BasicAuth  # type: ignore


class APIKeyAuth(BasicAuth):
    def check_auth(self, headers):
        api_key = headers.get("LIGHTHOUSE_API_KEY")

        if api_key:
            return api_key == current_app.config["LIGHTHOUSE_API_KEY"]
        return False

    def authorized(self, allowed_roles, resource, method):
        if (resource == "samples_declarations") and (method == "POST"):
            return self.check_auth(request.headers)
        else:
            return True
