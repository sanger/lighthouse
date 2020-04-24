import logging
import logging.config

from eve import Eve

from lighthouse.config.logging import LOGGING_CONF
from lighthouse.slack import send_message

logging.config.dictConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Eve(__name__, instance_relative_config=False)

    if test_config is None:
        # load the config, if it exists, when not testing
        app.config.from_pyfile("config/config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from lighthouse import plates

    app.register_blueprint(plates.bp)

    @app.route("/hello")
    def hello():
        logger.debug("hello")
        logger.error("hello")
        try:
            raise Exception("testing")
        except Exception as e:
            pass
        return "hello world"

    return app
