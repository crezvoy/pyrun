from unittest.mock import patch

import pytest

from pyrun.nsjail.nsjail import RunOutput


def test_wrong_method():
    # calling '/execute' with a wrong method should return a 405 response
    from pyrun import create_app

    app = create_app()
    with app.test_client() as client:
        response = client.get("/execute")
        assert response.status_code == 405
        assert b"Method Not Allowed" in response.data


def test_execute_invalid_input():
    from pyrun import create_app

    app = create_app()
    with app.test_client() as client:
        response = client.post("/execute", json={"code": "print('Hello, World!')"})
        assert response.status_code == 400
        assert b"Invalid request" in response.data


def test_execute_invalid_code():
    from pyrun import create_app

    app = create_app()
    with app.test_client() as client:
        response = client.post("/execute", json={"script": "print('Hello, World!')"})
        assert response.status_code == 400
        assert b"Invalid Python code" in response.data


def test_execute_valid_code_invalid_output():
    from pyrun import create_app

    code = """
def main():
    return "Hello, World!"
"""
    with patch(
        "pyrun.nsjail.run",
        return_value=(
            RunOutput(
                stdout="stdout",
                returncode=0,
                result="Hello, World!",
                nsjail_log="nsjail_log",
            )
        ),
    ).start():
        app = create_app()
        with app.test_client() as client:
            response = client.post("/execute", json={"script": code})
            print(response)
            assert response.status_code == 400
            assert b"Invalid JSON output" in response.data


def test_execute_valid_code_valid_output():
    from pyrun import create_app

    code = """
def main():
    return '{"output": "Hello, World!"}'
"""
    with patch(
        "pyrun.nsjail.run",
        return_value=(
            RunOutput(
                stdout="stdout",
                returncode=0,
                result='{"output": "Hello, World!"}',
                nsjail_log="nsjail_log",
            )
        ),
    ).start():
        app = create_app()
        with app.test_client() as client:
            response = client.post("/execute", json={"script": code})
            print(response)
            assert response.status_code == 200
            assert b'{"output": "Hello, World!"}' in response.data


if __name__ == "__main__":
    pytest.main(["-s", __file__])
