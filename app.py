"""Flask scientific calculator with safe expression evaluation."""

import ast
import math
import operator
import re
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

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

_TRIG = frozenset({"sin", "cos", "tan", "asin", "acos", "atan"})


def preprocess(expression: str) -> str:
    """Normalize symbols and insert implicit multiplication."""
    expr = expression.strip()
    expr = (
        expr.replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("–", "-")
        .replace("^", "**")
        .replace("π", "pi")
        .replace("√", "sqrt")
    )

    tokens = []
    i = 0
    n = len(expr)

    def peek_word(start: int) -> str | None:
        m = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", expr[start:])
        return m.group(0) if m else None

    def ends_value() -> bool:
        if not tokens:
            return False
        last = tokens[-1]
        return last in (")",) or last.replace(".", "", 1).isdigit() or last in _CONSTANTS

    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            while i < n and (expr[i].isdigit() or expr[i] == "."):
                i += 1
            if ends_value():
                tokens.append("*")
            tokens.append(expr[start:i])
            continue

        if ch == "(":
            if ends_value():
                tokens.append("*")
            tokens.append("(")
            i += 1
            continue

        if ch == ")":
            tokens.append(")")
            i += 1
            continue

        word = peek_word(i)
        if word:
            if ends_value():
                tokens.append("*")
            tokens.append(word)
            i += len(word)
            continue

        if ch in "+-*/%":
            if ch == "-" and (not tokens or tokens[-1] in ("(", "+", "-", "*", "/", "%", "**")):
                tokens.append(ch)
            else:
                if ends_value() and ch not in "+-":
                    pass
                tokens.append(ch)
            i += 1
            continue

        if ch == "*" and i + 1 < n and expr[i + 1] == "*":
            if ends_value():
                pass
            tokens.append("**")
            i += 2
            continue

        raise ValueError(f"Invalid character: {ch}")

    return "".join(tokens)


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

    def visit_Num(self, node):
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
        if name in _TRIG and self.use_degrees:
            if name in ("sin", "cos", "tan"):
                arg = math.radians(arg)
            else:
                return math.degrees(_MATH_FUNCS[name](arg))
        if name == "factorial":
            if isinstance(arg, float) and arg.is_integer():
                arg = int(arg)
            if not isinstance(arg, int) or arg < 0:
                raise ValueError("Factorial needs a non-negative integer")
        return _MATH_FUNCS[name](arg)

    def generic_visit(self, node):
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")


def format_result(value) -> str:
    """Format numeric results for display."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "Error"
        if math.isinf(value):
            return "Infinity"
        if abs(value) >= 1e12 or (abs(value) < 1e-8 and value != 0):
            return f"{value:.6g}"
        rounded = round(value, 10)
        if rounded == int(rounded):
            return str(int(rounded))
        text = f"{rounded:.8f}".rstrip("0").rstrip(".")
        return text
    return str(value)


def evaluate(expression: str, angle_mode: str = "deg"):
    """Parse and evaluate a math expression safely."""
    if not expression or not expression.strip():
        raise ValueError("Enter an expression")

    expr = preprocess(expression)
    tree = ast.parse(expr, mode="eval")
    use_degrees = angle_mode.lower() != "rad"
    result = SafeEvaluator(use_degrees=use_degrees).visit(tree)
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
        return jsonify({"ok": True, "result": result, "display": format_result(result)})
    except SyntaxError:
        return jsonify({"ok": False, "error": "Invalid expression"}), 400
    except ZeroDivisionError:
        return jsonify({"ok": False, "error": "Cannot divide by zero"}), 400
    except (ValueError, OverflowError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception:
        return jsonify({"ok": False, "error": "Invalid expression"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
