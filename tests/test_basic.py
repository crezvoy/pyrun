import pytest

from pyrun import create_app


def test_root():
    # calling '/' should return a 404 response
    app = create_app()
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 404
        assert b"Not Found" in response.data


if __name__ == "__main__":
    pytest.main(["-s", __file__])
