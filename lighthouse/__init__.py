import logging
import logging.config
from http import HTTPStatus

from eve import Eve
from flask_apscheduler import APScheduler

from lighthouse.validators.priority_samples import PrioritySamplesValidator

scheduler = APScheduler()


def create_app() -> Eve:
    app = Eve(__name__, validator=PrioritySamplesValidator)

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

    from lighthouse.blueprints import beckman, cherrypicked_plates, plate_events, plates, reports

    app.register_blueprint(plates.bp)
    app.register_blueprint(reports.bp)

    if app.config.get("BECKMAN_ENABLE", False):
        app.register_blueprint(beckman.bp)
        app.register_blueprint(cherrypicked_plates.bp)
        app.register_blueprint(plate_events.bp)

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
