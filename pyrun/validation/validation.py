import ast
from typing import Optional, Tuple


def validate_python_code(code: str) -> Tuple[bool, list[str]]:
    """
    Validate Python code passed as parameters. return True if the code is valid
    and False with a list of errors otherwise.
    """
    try:
        tree = ast.parse(code)
        if not isinstance(tree, ast.Module):
            return False, ["Invalid AST structure."]
        func: Optional[ast.stmt] = tree.body[0] if tree.body else None
        if not isinstance(func, ast.FunctionDef):
            return False, ["The code must contain a function definition."]
        if func is None or func.name != "main":
            return False, ["Function 'main' is not defined."]
        return True, []
    except SyntaxError as e:
        return False, [f"Syntax error: {e.msg} at line {e.lineno}"]
