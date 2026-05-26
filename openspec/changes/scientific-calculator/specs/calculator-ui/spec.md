## ADDED Requirements

### Requirement: Expression and result display

The UI SHALL show the current expression and the latest result. The result area SHALL show `0` when cleared.

#### Scenario: Clear display

- **WHEN** the user presses AC (clear)
- **THEN** the expression is empty and the result shows `0`

### Requirement: Scientific keypad

The UI SHALL provide buttons for digits `0-9`, decimal point, operators `+`, `−`, `×`, `÷`, `%`, parentheses, power (`xʸ`), constants `π` and `e`, and scientific functions: `sin`, `cos`, `tan`, inverse trig, `log`, `ln`, `√`, `n!`, `|x|`, `eˣ`. Pressing a button SHALL append the configured insert text to the expression.

#### Scenario: Insert from keypad

- **WHEN** the user clicks `7`, `+`, `3`
- **THEN** the expression display shows the concatenated inserts

### Requirement: Angle mode toggle

The UI SHALL provide DEG and RAD toggle buttons. The selected mode SHALL be sent as `angle_mode` on calculate requests.

#### Scenario: Switch to radians

- **WHEN** the user selects RAD and calculates `sin(1.5708)`
- **THEN** the request uses `angle_mode: "rad"`

### Requirement: Equals and server calculation

When the user triggers calculate (= button), the UI SHALL POST the expression and `angle_mode` to `/api/calculate`. On success, it SHALL display the result and MAY replace the expression with the result string for chained calculations.

#### Scenario: Successful equals

- **WHEN** the expression is `2+2` and the user presses =
- **THEN** the result display shows `4`

#### Scenario: Server error display

- **WHEN** the API returns `ok: false`
- **THEN** the UI shows the error message without crashing

### Requirement: Clear and backspace actions

The UI SHALL support AC to clear all and backspace (⌫) to remove the last character of the expression.

#### Scenario: Backspace

- **WHEN** the expression is `123` and the user presses backspace
- **THEN** the expression becomes `12`

### Requirement: Keyboard shortcuts

The UI SHALL support: `Enter` or `=` to calculate, `Esc` to clear, `Backspace` to delete last character, and direct typing of `0-9`, `.`, `+`, `-`, `*`, `/`, `(`, `)`, `%`, `^`.

#### Scenario: Enter calculates

- **WHEN** the user types `1+1` and presses Enter
- **THEN** the calculator performs the same action as pressing =

### Requirement: Responsive dark theme

The UI SHALL use a dark-themed, responsive layout readable on desktop and mobile widths.

#### Scenario: Viewport scaling

- **WHEN** the viewport width is reduced to mobile size
- **THEN** the keypad remains usable without horizontal overflow of the main calculator card

### Requirement: Network failure handling

If the fetch to `/api/calculate` fails (network error), the UI SHALL show a user-visible message such as "Could not reach server".

#### Scenario: Offline server

- **WHEN** the server is unreachable
- **THEN** the user sees a connection error message
