# expression-evaluation Specification

## Purpose
TBD - created by archiving change scientific-calculator. Update Purpose after archive.
## Requirements
### Requirement: Safe expression parsing

The evaluator SHALL parse user expressions using Python's `ast` module in `eval` mode and SHALL NOT use `eval()`, `exec()`, or `compile()` on user input.

#### Scenario: Reject unsupported syntax

- **WHEN** the expression contains attribute access, imports, lambdas, or comprehensions
- **THEN** evaluation fails with an error indicating unsupported syntax

### Requirement: Whitelisted numeric and operator nodes

The evaluator SHALL support numeric literals and these binary operators: `+`, `-`, `*`, `/`, `//`, `%`, `**` (or `^` after normalization). Unary `+` and `-` SHALL be supported.

#### Scenario: Basic arithmetic

- **WHEN** the expression is `2 + 3 * 4`
- **THEN** the result is `14`

#### Scenario: Power operator

- **WHEN** the expression is `2^3` or `2**3`
- **THEN** the result is `8`

#### Scenario: Division by zero

- **WHEN** the expression divides by zero
- **THEN** evaluation fails with a clear error

### Requirement: Whitelisted math functions

The evaluator SHALL support single-argument calls: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`, `log` (base 10), `ln`, `sqrt`, `abs`, `floor`, `ceil`, `exp`, `factorial`, `degrees`, `radians`. Each function SHALL accept exactly one positional argument and no keyword arguments.

#### Scenario: Square root

- **WHEN** the expression is `sqrt(16)`
- **THEN** the result is `4`

#### Scenario: Unknown function

- **WHEN** the expression calls an undefined function name
- **THEN** evaluation fails with an error naming the unknown function

### Requirement: Mathematical constants

The evaluator SHALL recognize the names `pi` and `e` as mathematical constants.

#### Scenario: Use pi in expression

- **WHEN** the expression is `2 * pi` (after normalization from `π` if present)
- **THEN** the result approximates `2π`

### Requirement: Symbol normalization

Before parsing, the system SHALL normalize calculator symbols: `×` → `*`, `÷` → `/`, `π` → `pi`, `√` → `sqrt`, `^` → `**`.

#### Scenario: UI division symbol

- **WHEN** the expression is `10 ÷ 2`
- **THEN** the result is `5`

### Requirement: Angle mode for trigonometry

The evaluator SHALL accept `angle_mode` of `deg` or `rad` (default `deg`). In `deg` mode, `sin`, `cos`, and `tan` SHALL treat their argument as degrees. In `deg` mode, `asin`, `acos`, and `atan` SHALL return degrees. In `rad` mode, arguments and results SHALL use radians with no conversion.

#### Scenario: Sine in degrees

- **WHEN** `angle_mode` is `deg` and the expression is `sin(90)`
- **THEN** the result is `1`

#### Scenario: Sine in radians

- **WHEN** `angle_mode` is `rad` and the expression is `sin(1.5707963267948966)`
- **THEN** the result is approximately `1`

### Requirement: Empty and invalid expressions

The evaluator SHALL reject empty or whitespace-only expressions. Syntax errors SHALL produce a failure with a parse or validation message.

#### Scenario: Empty expression

- **WHEN** the expression is empty or only whitespace
- **THEN** evaluation fails with an error indicating an empty expression

### Requirement: Integer-friendly results

When a floating-point result represents a whole number, the system SHALL return an integer value (e.g. `9` instead of `9.0`).

#### Scenario: Whole number result

- **WHEN** the expression is `sin(90) + 2^3` in `deg` mode
- **THEN** the result is `9`

