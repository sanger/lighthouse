import logging
import logging.config
from http import HTTPStatus

from eve import Eve
from flask_apscheduler import APScheduler

from lighthouse.hooks.cherrypick_test_data import inserted_cherrypick_test_data_hook
from lighthouse.hooks.events import insert_events_hook, inserted_events_hook
from lighthouse.routes import eve_routes
from lighthouse.routes.v1 import beckman_routes as v1_beckman_routes
from lighthouse.routes.v1 import routes as v1_routes
from lighthouse.routes.v3 import beckman_routes as v3_beckman_routes
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
    # When registering blueprints, do so both in the root and in versioned endpoints such as /v1.
    # Register latest version routes at the root of the API -- note that Eve automatically registered at the root.
    app.register_blueprint(v1_routes.bp, name="root_routes")
    app.register_blueprint(v3_beckman_routes.bp, name="root_beckman_routes")

    # Register /v1 routes
    app.register_blueprint(eve_routes.bp, url_prefix="/v1")
    app.register_blueprint(v1_routes.bp, url_prefix="/v1")
    app.register_blueprint(v1_beckman_routes.bp, url_prefix="/v1")

    # Register /v3 routes (there is no /v2)
    app.register_blueprint(v3_beckman_routes.bp, url_prefix="/v3")
