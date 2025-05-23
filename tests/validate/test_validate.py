import pytest

from pyrun.validation import validate_python_code


def test_empty_code():
    # Test empty code
    code = ""
    is_valid, errors = validate_python_code(code)
    assert not is_valid
    assert errors == ["The code must contain a function definition."]


def test_no_function_def():
    # Test empty code
    code = """var = 1
    """
    is_valid, errors = validate_python_code(code)
    assert not is_valid
    assert errors == ["The code must contain a function definition."]


def test_syntax_error():
    code = """this is not python code"""
    is_valid, errors = validate_python_code(code)
    assert not is_valid
    assert len(errors) == 1
    assert errors[0].startswith("Syntax error: ")


def test_no_main():
    code = """
def hello_world():
    print("Hello world!")
    """
    is_valid, errors = validate_python_code(code)
    assert not is_valid
    assert errors == ["Function 'main' is not defined."]


def test_valid():
    code = """
def main():
    print("Hello world!")

    """
    is_valid, _ = validate_python_code(code)
    assert is_valid


if __name__ == "__main__":
    pytest.main(["-s", __file__])
