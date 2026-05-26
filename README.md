# Scientific Calculator (Flask)

A web-based scientific calculator built with [Flask](https://flask.palletsprojects.com/). Expressions are evaluated on the server using a restricted AST parser—no unsafe `eval()`.

This project is built with **Specification-Driven Development (SDD)** using [OpenSpec](https://github.com/Fission-AI/OpenSpec). Requirements live under `openspec/changes/scientific-calculator/` (proposal, design, specs, tasks). Run `openspec status --change scientific-calculator` to inspect the change.

## Features

- Basic arithmetic: `+`, `−`, `×`, `÷`, `%`, parentheses
- Scientific functions: `sin`, `cos`, `tan`, inverse trig, `log`, `ln`, `sqrt`, powers, factorial, `abs`, `exp`
- Constants: `π` (pi), `e`
- Angle modes: **DEG** (degrees) and **RAD** (radians)
- Keyboard shortcuts for faster input
- Responsive dark-themed UI

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

## Usage

### On-screen buttons

Click number and operator keys to build an expression, then press **=** to calculate.

Toggle **DEG** / **RAD** at the top for trigonometric functions:

| Mode | Example | Result |
|------|---------|--------|
| DEG  | `sin(90)` | `1` |
| RAD  | `sin(1.5708…)` | `1` |

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
├── app.py                 # Flask app and safe expression evaluator
├── requirements.txt       # Python dependencies
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
  "result": 9
}
```

**Error response (400):**

```json
{
  "ok": false,
  "error": "Invalid expression"
}
```

### Supported expression syntax

- Operators: `+`, `-`, `*`, `/`, `%`, `**` or `^` for power
- Functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `log`, `ln`, `sqrt`, `abs`, `floor`, `ceil`, `exp`, `factorial`, `degrees`, `radians`
- Constants: `pi`, `e`
- Aliases in UI: `×` → `*`, `÷` → `/`, `π` → `pi`, `√` → `sqrt`

## Security

Expressions are parsed with Python’s `ast` module and only whitelisted nodes (numbers, names, binary/unary ops, and approved math calls) are evaluated. Arbitrary code execution is not possible.

## License

Use and modify freely for learning and workshop purposes.
