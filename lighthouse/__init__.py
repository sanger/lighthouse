import logging
import logging.config
from http import HTTPStatus
from typing import Dict

from eve import Eve  # type: ignore

from lighthouse.config.logging import LOGGING_CONF
from lighthouse.config.settings import SETTINGS

logging.config.dictConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)


def create_app(test_config: Dict[str, str] = None, test_settings: Dict[str, str] = None) -> Eve:
    settings = SETTINGS if test_settings is None else test_settings

    app = Eve(__name__, settings=settings, instance_relative_config=False)

    if test_config is None:
        # load the config, if it exists, when not testing
        app.config.from_pyfile("config/config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from lighthouse import plates

    app.register_blueprint(plates.bp)

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
