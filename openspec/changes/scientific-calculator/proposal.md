## Why

The workshop currently has a working scientific calculator built through ad-hoc “vibe coding,” without written requirements or traceability from behavior to code. Specification-Driven Development (SDD) with OpenSpec fixes that by defining capabilities, acceptance criteria, and implementation tasks before and during build—so features are verifiable, security constraints are explicit, and future changes stay aligned with documented behavior.

## What Changes

- Introduce OpenSpec capabilities and requirement specs for the scientific calculator (replacing implicit vibe-coded behavior).
- Implement (or align) a Flask web app with server-side safe expression evaluation—no unsafe `eval()`.
- Deliver a responsive scientific calculator UI: display, keypad, DEG/RAD toggle, keyboard shortcuts.
- Document and enforce: supported operators, functions, constants, symbol normalization, angle modes, and error handling.
- Add a `POST /api/calculate` JSON API contract with structured success and error responses.
- Provide README and project structure consistent with the specs.

## Capabilities

### New Capabilities

- `expression-evaluation`: Safe parsing and evaluation of math expressions (AST whitelist, operators, scientific functions, constants, DEG/RAD handling, symbol normalization, error cases).
- `calculator-api`: HTTP API for evaluating expressions (`POST /api/calculate`) with JSON request/response schema.
- `calculator-ui`: Browser UI—expression/result display, scientific keypad, angle mode toggle, keyboard input, API integration.

### Modified Capabilities

<!-- None — greenfield specs under openspec/changes/ -->

## Impact

- **Code**: `app.py`, `templates/index.html`, `static/css/style.css`, `static/js/calculator.js`, `requirements.txt`, `README.md`
- **API**: New or aligned `POST /api/calculate` endpoint
- **Dependencies**: Python 3.8+, Flask 3.0+
- **Process**: Artifacts live under `openspec/changes/scientific-calculator/`; archived specs will land in `openspec/specs/` when the change is completed
