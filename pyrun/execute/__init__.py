from flask import Blueprint

bp = Blueprint("execute", __name__)


from pyrun.execute import routes as routes  # noqa: E402
