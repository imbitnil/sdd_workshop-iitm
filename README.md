# Scientific Calculator (Flask)

A web-based scientific calculator built with [Flask](https://flask.palletsprojects.com/). Expressions are evaluated on the server using a restricted AST parser—no unsafe `eval()`.

## Features

- Basic arithmetic: `+`, `−`, `×`, `÷`, `%` (modulo), parentheses
- Scientific functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `ln`, `sqrt`, powers, factorial, `abs`, `exp`
- Constants: `π` (pi), `e`
- **Implicit multiplication** — `2pi`, `2e`, and `2sin(90)` work without typing `*`
- Angle modes: **DEG** (degrees) and **RAD** (radians)
- Chain calculations after pressing `=` (continue with operators or start fresh with digits)
- Keyboard shortcuts
- Responsive dark-themed UI with monospace display

## Requirements

- Python 3.8+
- Flask 3.0+

## Installation

```bash
git clone <your-repo-url>
cd workshop-iitm
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

> **Important:** Start the app with `python app.py`. Do not open `templates/index.html` directly in the browser—static files and the `/api/calculate` endpoint require the Flask server.

## Usage

### On-screen buttons

Click keys to build an expression, then press **=** to calculate.

| Example | Result (DEG) |
|---------|----------------|
| `sin(90)` | `1` |
| `2` + `π` | ~`6.28` |
| `2` + `^` + `10` | `1024` |
| `2` + `sin` + `(90)` | `2` (implicit `2*sin(90)`) |

Toggle **DEG** / **RAD** at the top for trigonometric functions.

### Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Enter` or `=` | Calculate |
| `Esc` | Clear (AC) |
| `Backspace` | Delete last character |
| `0–9`, `.`, `+`, `-`, `*`, `/`, `(`, `)`, `%`, `^` | Insert into expression |

## Project structure

```
workshop-iitm/
├── app.py                 # Flask app, preprocessor, and safe evaluator
├── requirements.txt       # Python dependencies
├── README.md
├── templates/
│   └── index.html         # Calculator page
└── static/
    ├── css/
    │   └── style.css      # Styles
    └── js/
        └── calculator.js  # UI logic and API calls
```

## API

### `POST /api/calculate`

Evaluate a math expression.

**Request body (JSON):**

```json
{
  "expression": "sin(90) + 2^3",
  "angle_mode": "deg"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `expression` | string | Math expression to evaluate |
| `angle_mode` | string | `"deg"` or `"rad"` (default: `"deg"`) |

**Success response (200):**

```json
{
  "ok": true,
  "result": 9,
  "display": "9"
}
```

| Field | Description |
|-------|-------------|
| `result` | Raw numeric result (number) |
| `display` | Formatted string for the UI (trailing zeros removed, scientific notation for very large/small values) |

**Error response (400):**

```json
{
  "ok": false,
  "error": "Cannot divide by zero"
}
```

### Supported expression syntax

- Operators: `+`, `-`, `*`, `/`, `%`, `**` or `^` for power
- Functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `ln`, `sqrt`, `abs`, `floor`, `ceil`, `exp`, `factorial`, `degrees`, `radians`
- Constants: `pi`, `e`
- Implicit multiplication: `2pi` → `2*pi`, `3(4)` → `3*(4)`, `2sin(90)` → `2*sin(90)`
- UI symbol aliases: `×` → `*`, `÷` → `/`, `π` → `pi`, `√` → `sqrt`, `−` → `-`

## Security

Expressions are parsed with Python’s `ast` module and only whitelisted nodes (numbers, names, binary/unary ops, and approved math calls) are evaluated. Arbitrary code execution is not possible.

## License

Use and modify freely for learning and workshop purposes.
