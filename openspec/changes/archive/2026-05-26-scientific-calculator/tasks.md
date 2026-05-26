## 1. Project setup

- [x] 1.1 Add `requirements.txt` with Flask 3.0+ and document Python 3.8+ in README
- [x] 1.2 Ensure project structure matches design (`app.py`, `templates/`, `static/`)

## 2. Expression evaluation (expression-evaluation spec)

- [x] 2.1 Implement `SafeEvaluator` with AST whitelist (no `eval()`)
- [x] 2.2 Add symbol normalization (`×`, `÷`, `π`, `√`, `^`)
- [x] 2.3 Implement DEG/RAD handling for trig and inverse trig
- [x] 2.4 Handle errors: empty expression, syntax, domain, division by zero, overflow

## 3. Calculator API (calculator-api spec)

- [x] 3.1 Implement `GET /` serving calculator template
- [x] 3.2 Implement `POST /api/calculate` with JSON contract and status codes

## 4. Calculator UI (calculator-ui spec)

- [x] 4.1 Build `index.html` with display, DEG/RAD toggle, and scientific keypad
- [x] 4.2 Implement `calculator.js` (insert, clear, backspace, fetch API, keyboard)
- [x] 4.3 Style responsive dark theme in `style.css`

## 5. Documentation and verification

- [x] 5.1 Update README with install, run, API, and keyboard shortcuts
- [x] 5.2 Manually verify spec scenarios: `sin(90)` DEG, `2+2`, errors, keyboard
