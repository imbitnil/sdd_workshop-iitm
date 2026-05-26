"""Flask scientific calculator with safe expression evaluation."""

import ast
import math
import operator
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Allowed binary operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Math functions exposed to expressions (radians unless noted)
_MATH_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
    "exp": math.exp,
    "factorial": math.factorial,
    "degrees": math.degrees,
    "radians": math.radians,
}

_CONSTANTS = {"pi": math.pi, "e": math.e}


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate a restricted subset of Python AST nodes."""

    def __init__(self, use_degrees: bool = True):
        self.use_degrees = use_degrees

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    def visit_Num(self, node):  # Python < 3.8
        return node.n

    def visit_Name(self, node):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError("Unsupported operator")
        if op_type is ast.Pow and isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if left < 0 and not float(right).is_integer():
                raise ValueError("Invalid power for negative base")
        return _BIN_OPS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError("Unsupported unary operator")
        return _UNARY_OPS[op_type](operand)

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        name = node.func.id
        if name not in _MATH_FUNCS:
            raise ValueError(f"Unknown function: {name}")
        if len(node.args) != 1 or node.keywords:
            raise ValueError(f"{name}() expects exactly one argument")
        arg = self.visit(node.args[0])
        if name in ("sin", "cos", "tan", "asin", "acos", "atan") and self.use_degrees:
            if name in ("sin", "cos", "tan"):
                arg = math.radians(arg)
            else:
                result = _MATH_FUNCS[name](arg)
                return math.degrees(result)
        return _MATH_FUNCS[name](arg)

    def generic_visit(self, node):
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def evaluate(expression: str, angle_mode: str = "deg") -> float:
    """Parse and evaluate a math expression safely."""
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Normalize common calculator symbols
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    expr = expr.replace("π", "pi").replace("√", "sqrt")

    tree = ast.parse(expr, mode="eval")
    use_degrees = angle_mode.lower() != "rad"
    result = SafeEvaluator(use_degrees=use_degrees).visit(tree)

    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    expression = data.get("expression", "")
    angle_mode = data.get("angle_mode", "deg")

    try:
        result = evaluate(expression, angle_mode)
        return jsonify({"ok": True, "result": result})
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({"ok": False, "error": "Invalid expression"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
