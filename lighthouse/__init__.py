import logging
import logging.config
from http import HTTPStatus

from eve import Eve  # type: ignore
from flask_apscheduler import APScheduler  # type: ignore

scheduler = APScheduler()


def create_app(test_config_path: str = None) -> Eve:

    if test_config_path is None:
        # load the config from the environmental variable 'EVE_SETTINGS'
        app = Eve(__name__)
    else:
        # load the test config passed in
        app = Eve(__name__, settings=test_config_path)

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

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
