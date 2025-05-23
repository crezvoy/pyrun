import json
import time

import structlog
from flask import g, request
from flask.typing import ResponseReturnValue

import pyrun.nsjail as nsjail
from pyrun.execute import bp
from pyrun.validation import validate_python_code

BadRequest = 400
OK = 200


@bp.route("/execute", methods=["POST"])
def execute() -> ResponseReturnValue:
    logger = structlog.get_logger().bind(ip=request.remote_addr).bind(id=g.rid)
    logger.info("processing request: %s", request.get_data())
    start_time = time.time()
    request_data = request.get_json()
    if not request_data or "script" not in request_data:
        logger.info("missing script")
        return "Invalid request", BadRequest
    script = request_data["script"]
    valid, errors = validate_python_code(script)
    if not valid:
        error_messages = "\n - ".join(errors)
        logger.bind(errors=error_messages).info("invalid code")
        return f"Invalid Python code: \n - {error_messages}", BadRequest
    res = nsjail.run(script)
    if res.returncode != 0:
        logger.bind(return_code=res.returncode).bind(nsjail_log=res.nsjail_log).bind(
            stdout=res.stdout
        ).info("nsjail failed")
        return (
            f"Python code execution failed ({res.returncode}): {res.stdout}",
            BadRequest,
        )
    try:
        json_res = json.loads(res.result)
    except json.JSONDecodeError:
        logger.bind(result=res.result).info("invalid json output")
        return f"Invalid JSON output: {res.result}", BadRequest

    logger.bind(duration=time.time() - start_time).info(
        "request processed successfully"
    )

    return (
        json.dumps(
            {
                "stdout": res.stdout,
                "result": json_res,
            }
        ),
        OK,
    )
