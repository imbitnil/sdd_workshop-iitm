# Specification-Driven Development (SDD)

This project was built with **OpenSpec** spec-driven workflow—not ad-hoc vibe coding. Requirements were written first; implementation was checked against them.

## Workflow

```text
proposal.md  →  specs/**/*.md  →  design.md  →  tasks.md  →  code
   (why)          (what)            (how)         (steps)      (app)
```

| Step | Artifact | Location |
|------|----------|----------|
| 1 | Proposal | `openspec/changes/archive/2026-05-26-scientific-calculator/proposal.md` |
| 2 | Specs | `openspec/specs/<capability>/spec.md` |
| 3 | Design | `openspec/changes/archive/2026-05-26-scientific-calculator/design.md` |
| 4 | Tasks | `openspec/changes/archive/2026-05-26-scientific-calculator/tasks.md` |
| 5 | Code | `app.py`, `templates/`, `static/` |

After archive, canonical requirements live under **`openspec/specs/`**.

## Capabilities → code traceability

| Capability | Spec | Implemented in |
|------------|------|------------------|
| `expression-evaluation` | `openspec/specs/expression-evaluation/spec.md` | `app.py` — `SafeEvaluator`, `evaluate()` |
| `calculator-api` | `openspec/specs/calculator-api/spec.md` | `app.py` — routes `/`, `/api/calculate` |
| `calculator-ui` | `openspec/specs/calculator-ui/spec.md` | `templates/index.html`, `static/js/calculator.js`, `static/css/style.css` |

## What is *not* specified (implementation detail)

- Exact colors/fonts (theme changed post-spec; spec requires responsive cohesive theme only)
- Flask `debug=True` for local workshop use

## Verify alignment

```bash
openspec validate --specs
openspec list --specs
python -c "from app import evaluate; assert evaluate('sin(90)+2^3','deg')==9"
```

## Contrast: vibe coding branch

The repo may include a `vibe_coded_submission` branch built without OpenSpec artifacts. This branch (`sdd_submission` / main with SDD) should include `openspec/specs/` and this file.
