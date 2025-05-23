import os
import subprocess
import tempfile

from jinja2 import Template

from pyrun.nsjail.config import nsconfig

NSJAIL_TIMEOUT = 10  # seconds

wrapper = """
#!/bin/env python3
import sys
from os import path

{main_func}

output_file = sys.argv[1]

res = main()

with open(output_file, "w") as f:
    f.write(str(res))
"""


class RunOutput:
    def __init__(self, stdout: str, returncode: int, result: str, nsjail_log: str):
        self.stdout = stdout
        self.returncode = returncode
        self.result = result
        self.nsjail_log = nsjail_log

    def __repr__(self):
        return f"RunOutput(stdout={self.stdout}, result={self.result} returncode={self.returncode}"


def run(script: str) -> RunOutput:
    # Create a temporary directory for the script
    with tempfile.TemporaryDirectory() as process_dir:
        script_file = os.path.join(process_dir, "script.py")
        with open(script_file, "w") as f:
            f.write(wrapper.format(main_func=script))
        result_file = os.path.join(process_dir, "result.txt")
        open(result_file, "w").close()
        nsjail_log_file = os.path.join(process_dir, "nsjail.log")
        # open(result_file, "w").close()
        nsjail_config_file = os.path.join(process_dir, "nsjail.cfg")
        with open(nsjail_config_file, "w") as f:
            template = Template(nsconfig)
            f.write(
                template.render(process_dir=process_dir, NSJAIL_TIMEOUT=NSJAIL_TIMEOUT)
            )

        # Make the script executable
        os.chmod(script_file, 0o755)

        # Run the script in a sandboxed environment using nsjail
        command = [
            "nsjail",
            "--config",
            nsjail_config_file,
            "--log",
            nsjail_log_file,
            "--",
            "/usr/local/bin/python",
            "/tmp/script.py",
            "/tmp/result.txt",
        ]

        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        nsjail_log_file = os.path.join(process_dir, "nsjail.log")
        with open(nsjail_log_file, "r") as f:
            nsjail_log = f.read()

        if result.returncode != 0:
            # check is a timeout occurred
            with open(nsjail_log_file, "r") as f:
                log_content = f.read()
                print(log_content)
                if "time >= time_limit" in log_content:
                    return RunOutput(
                        stdout=result.stdout,
                        returncode=result.returncode,
                        result='{"error": "Timeout"}',
                        nsjail_log=log_content,
                    )
                else:
                    return RunOutput(
                        stdout=result.stdout,
                        returncode=result.returncode,
                        result='{"error": "Unknown error"}',
                        nsjail_log=log_content,
                    )

        with open(result_file, "r") as f:
            result_content = f.read()

        return RunOutput(
            stdout=result.stdout,
            returncode=result.returncode,
            result=result_content,
            nsjail_log=nsjail_log,
        )
