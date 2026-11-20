"""
safe_formula_eval.py — Safe spectral formula evaluator using Python's ast module.

Replaces eval() with an AST-based whitelist parser that only permits:
  - Band identifiers: B02, B03, B04, B08, B11, B12
  - Numeric literals (int and float)
  - Binary operators: +, -, *, /
  - Unary operators: -, +
  - Parentheses (grouping)

Any other node — imports, function calls, attribute access, subscripts,
comparisons, comprehensions — raises a ValueError before numpy ever runs.

This prevents remote code execution via the /api/raster/eval-formula endpoint.
"""

import ast
import numpy as np
from typing import Dict

# The only names allowed inside a formula
ALLOWED_NAMES = {"B02", "B03", "B04", "B08", "B11", "B12"}

# The only AST node types allowed anywhere in the tree
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Expression,
    # Literals
    ast.Constant,
    # Names (band variables only — checked separately)
    ast.Name,
    ast.Load,
    # Arithmetic
    ast.BinOp,
    ast.UnaryOp,
    # Allowed operators
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.UAdd,
    ast.USub,
)


class _SafeFormulaVisitor(ast.NodeVisitor):
    """Walk the AST and raise ValueError on any disallowed node."""

    def generic_visit(self, node: ast.AST) -> None:
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(
                f"Disallowed expression type '{type(node).__name__}' in formula. "
                "Only band variables (B02 B03 B04 B08 B11 B12), numbers, "
                "and +  -  *  /  ( ) are permitted."
            )
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id not in ALLOWED_NAMES:
            raise ValueError(
                f"Unknown name '{node.id}'. "
                f"Allowed band variables: {sorted(ALLOWED_NAMES)}"
            )


def _eval_node(node: ast.AST, bands: Dict[str, np.ndarray]) -> np.ndarray:
    """Recursively evaluate a validated AST node against band arrays."""
    if isinstance(node, ast.Constant):
        return float(node.value)
    if isinstance(node, ast.Name):
        return bands[node.id]
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, bands)
        right = _eval_node(node.right, bands)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            # Epsilon guard prevents NaN/Inf from zero-division
            denom = np.where(np.abs(right) < 1e-9, 1e-9, right)
            return left / denom
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, bands)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return operand
    raise ValueError(f"Unexpected AST node: {type(node).__name__}")


def safe_eval_formula(formula: str, bands: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Parse and evaluate a spectral index formula safely.

    Parameters
    ----------
    formula : str
        Expression using band names and arithmetic, e.g. "(B08 - B04) / (B08 + B04)"
    bands : dict
        Mapping of band name → numpy array (must include all names used in formula)

    Returns
    -------
    np.ndarray
        Evaluated result array, with NaN/Inf replaced by 0.0 / ±1.0

    Raises
    ------
    ValueError
        If the formula contains disallowed tokens or names
    SyntaxError
        If the formula is not valid Python syntax
    """
    if not formula or not formula.strip():
        raise ValueError("Formula cannot be empty")

    if len(formula) > 256:
        raise ValueError("Formula too long (max 256 characters)")

    # Parse to AST — raises SyntaxError on bad input
    try:
        tree = ast.parse(formula.strip(), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Formula syntax error: {exc}") from exc

    # Whitelist check — raises ValueError on any disallowed node
    _SafeFormulaVisitor().visit(tree)

    # Evaluate using the validated AST (no eval() involved)
    result = _eval_node(tree.body, bands)

    # Coerce scalar to array for uniform downstream handling
    if not isinstance(result, np.ndarray):
        result = np.full(next(iter(bands.values())).shape, float(result))

    return np.nan_to_num(result, nan=0.0, posinf=1.0, neginf=-1.0)
