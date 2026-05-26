## Context

Workshop participants need a scientific calculator that is safe, teachable, and spec-driven. The stack is a small Flask monolith: server renders one page, static assets handle UI, and expression evaluation runs on the server. A prior vibe-coded branch exists as reference behavior; this change codifies requirements in OpenSpec and implements (or aligns) code to match.

Constraints: Python 3.8+, Flask 3.0+, no `eval()` on user input, minimal dependencies, suitable for local workshop use (single process, debug-friendly).

## Goals / Non-Goals

**Goals:**

- Safe AST-based evaluation with an explicit whitelist of nodes, operators, functions, and constants.
- DEG/RAD modes for trigonometry and inverse trigonometry.
- REST JSON API and browser UI that match the capability specs.
- Clear error messages for invalid syntax, unknown symbols, domain errors, and division by zero.
- Responsive themed UI with keyboard shortcuts (styling via CSS variables in `static/css/style.css`).

**Non-Goals:**

- Graphing, unit conversion, programming mode, or complex numbers.
- User accounts, history persistence, or multi-tenant deployment.
- Client-side-only evaluation (security and consistency stay server-side).
- Mobile native apps or PWA offline support.

## Decisions

### 1. Server-side evaluation via `ast` (not `eval`)

**Choice:** Parse expressions with `ast.parse(..., mode="eval")` and walk the tree with a custom `NodeVisitor` that only allows approved node types.

**Rationale:** Blocks arbitrary code execution while supporting a rich math surface. Alternatives: `numexpr` (extra dependency), client-side math.js (duplicated logic and weaker security story for a security workshop).

### 2. Monolithic Flask app

**Choice:** Single `app.py` with routes `/` and `/api/calculate`, Jinja template, static CSS/JS.

**Rationale:** Lowest ceremony for a workshop; specs remain modular via OpenSpec capabilities. Alternative: API + SPA split—rejected as over-engineering for scope.

### 3. Angle mode applied in the evaluator

**Choice:** `angle_mode` (`deg` | `rad`) passed into `SafeEvaluator`; trig inputs converted to radians in DEG mode; inverse trig results converted to degrees in DEG mode.

**Rationale:** Matches common calculator UX (`sin(90)` → `1` in DEG). Alternative: require users to always use radians—rejected for usability.

### 4. Symbol normalization before parse

**Choice:** Replace UI symbols (`×`, `÷`, `π`, `√`, `^`) with Python equivalents (`*`, `/`, `pi`, `sqrt`, `**`) in one preprocessing step.

**Rationale:** Keeps the parser simple and allows both keyboard and button input. Documented in the expression-evaluation spec.

### 5. JSON API contract

**Choice:** `POST /api/calculate` with `{ "expression", "angle_mode" }` → `{ "ok", "result" }` or `{ "ok": false, "error" }` with HTTP 400 on failure.

**Rationale:** Easy to test with curl and to wire from `fetch` in the UI.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| AST whitelist misses an unsafe node type | `generic_visit` raises on any unlisted node; code review against spec |
| Float precision surprises | Document behavior; return integers when result is mathematically integral |
| Factorial / large powers cause overflow | Catch `OverflowError`; return clear error |
| UI and server symbol sets drift | Single normalization list in server; UI inserts documented aliases |

## Migration Plan

1. Land OpenSpec artifacts (proposal, specs, design, tasks).
2. Implement or align `app.py`, template, static assets, and README per tasks.
3. Verify scenarios manually (DEG/RAD, operators, errors, keyboard).
4. Archive change to `openspec/specs/` when complete.
5. Workshop branch strategy: `sdd_submission` holds spec-driven work; `vibe_coded_submission` remains as contrast.

## Open Questions

- None blocking implementation; optional future: automated tests mapped to spec scenarios.
