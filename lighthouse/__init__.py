import logging
import logging.config
from http import HTTPStatus

from eve import Eve  # type: ignore
from flask_apscheduler import APScheduler  # type: ignore
from lighthouse.authorization import APIKeyAuth
from lighthouse.validators.samples_declarations import (
    pre_samples_declarations_post_callback,
    post_samples_declarations_post_callback,
    SamplesDeclarationsValidator,
)

scheduler = APScheduler()


def create_app() -> Eve:
    app = Eve(__name__, validator=SamplesDeclarationsValidator, auth=APIKeyAuth)
    app.on_pre_POST_samples_declarations += pre_samples_declarations_post_callback
    app.on_post_POST_samples_declarations += post_samples_declarations_post_callback

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

    from lighthouse.blueprints import plates
    from lighthouse.blueprints import dart_plates
    from lighthouse.blueprints import reports

    app.register_blueprint(plates.bp)
    app.register_blueprint(dart_plates.bp)
    app.register_blueprint(reports.bp)

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
