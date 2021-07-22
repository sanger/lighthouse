import logging
import logging.config
from http import HTTPStatus

from eve import Eve
from flask_apscheduler import APScheduler

from lighthouse.hooks.cherrypick_test_data import inserted_cherrypick_test_data_hook
from lighthouse.hooks.events import insert_events_hook, inserted_events_hook
from lighthouse.validator import LighthouseValidator

scheduler = APScheduler()


def create_app() -> Eve:
    app = Eve(__name__, validator=LighthouseValidator)

    # Fired before inserting entities
    app.on_insert_events += insert_events_hook

    # Fired after entities are inserted
    app.on_inserted_events += inserted_events_hook
    app.on_inserted_cherrypick_test_data += inserted_cherrypick_test_data_hook

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    setup_routes(app)

    @app.get("/health")
    def _():
        """Confirms the health of Lighthouse by confirming it is responding to requests."""
        return "Factory working", HTTPStatus.OK

    return app


def setup_routes(app):
    # Register the v1 endpoints for the Eve API.  Note that Eve automatically registers endpoints at the root.
    from lighthouse.routes import eve_routes

    app.register_blueprint(eve_routes.bp, url_prefix="/v1")

    # When registering blueprints, do so both in the root and in /v1.
    # Future versions will just be appended to the bottom of these registrations.
    from lighthouse.routes.v1 import routes as v1_routes

    app.register_blueprint(v1_routes.bp)
    app.register_blueprint(v1_routes.bp, url_prefix="/v1")

    if app.config.get("BECKMAN_ENABLE", False):
        from lighthouse.routes.v1 import beckman_routes as v1_beckman_routes

        app.register_blueprint(v1_beckman_routes.bp)
        app.register_blueprint(v1_beckman_routes.bp, url_prefix="/v1")
