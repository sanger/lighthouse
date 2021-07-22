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
    from lighthouse.blueprints import beckman, cherrypicked_plates, eve_routes, plate_events, plates, reports

    app.register_blueprint(eve_routes.bp, url_prefix="/v1")
    app.register_blueprint(plates.bp, url_prefix="/v1")
    app.register_blueprint(reports.bp, url_prefix="/v1")

    if app.config.get("BECKMAN_ENABLE", False):
        app.register_blueprint(beckman.bp, url_prefix="/v1")
        app.register_blueprint(cherrypicked_plates.bp, url_prefix="/v1")
        app.register_blueprint(plate_events.bp, url_prefix="/v1")
