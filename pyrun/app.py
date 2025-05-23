import uuid

import structlog
from flask import Flask, g

from pyrun.execute import bp as execute


def create_app() -> Flask:
    logger = structlog.get_logger()
    logger.info("Creating Flask app")
    from flask import Flask

    app = Flask(__name__)

    @app.before_request
    def add_request_id():
        g.rid = str(uuid.uuid4())

    app.register_blueprint(execute)

    return app
