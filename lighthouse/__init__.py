import logging
import logging.config
from http import HTTPStatus

from eve import Eve  # type: ignore
from flask_apscheduler import APScheduler  # type: ignore

scheduler = APScheduler()


def create_app() -> Eve:
    app = Eve(__name__)

    # setup logging
    # logging.config.dictConfig(app.config["LOGGING"])

    from lighthouse.blueprints import plates
    from lighthouse.blueprints import reports

    app.register_blueprint(plates.bp)
    app.register_blueprint(reports.bp)

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
