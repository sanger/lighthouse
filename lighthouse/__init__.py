import logging
import logging.config
from http import HTTPStatus

from eve import Eve
from flask_apscheduler import APScheduler

from lighthouse.hooks.events import insert_events_hook, inserted_events_hook
from lighthouse.validator import LighthouseValidator

scheduler = APScheduler()


def create_app() -> Eve:
    app = Eve(__name__, validator=LighthouseValidator)

    # Fired before inserting the event
    app.on_insert_events += insert_events_hook

    # Fired after the event is inserted
    app.on_inserted_events += inserted_events_hook

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

    from lighthouse.blueprints import (
        beckman,
        cherrypicked_plates,
        cherrypicker_test_data,
        plate_events,
        plates,
        reports,
    )

    app.register_blueprint(plates.bp)
    app.register_blueprint(reports.bp)

    if app.config.get("BECKMAN_ENABLE", False):
        app.register_blueprint(beckman.bp)
        app.register_blueprint(cherrypicked_plates.bp)
        app.register_blueprint(plate_events.bp)

    if app.config.get("CHERRYPICKER_ENABLED", False):
        app.register_blueprint(cherrypicker_test_data.bp)

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    @app.get("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
