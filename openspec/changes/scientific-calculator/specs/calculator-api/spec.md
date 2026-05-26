## ADDED Requirements

### Requirement: Calculate endpoint

The application SHALL expose `POST /api/calculate` that accepts JSON and returns JSON.

#### Scenario: Successful calculation

- **WHEN** the client sends `POST /api/calculate` with body `{"expression": "2+2", "angle_mode": "deg"}`
- **THEN** the response status is 200 and the body is `{"ok": true, "result": 4}`

### Requirement: Request body fields

The endpoint SHALL read `expression` as a string and `angle_mode` as an optional string (`deg` or `rad`). If `angle_mode` is omitted, it SHALL default to `deg`.

#### Scenario: Default angle mode

- **WHEN** the client sends only `{"expression": "sin(90)"}`
- **THEN** the result is computed using degree mode

### Requirement: Error responses

On evaluation failure, the endpoint SHALL return HTTP 400 with body `{"ok": false, "error": "<message>"}` where `<message>` describes the failure.

#### Scenario: Invalid expression error

- **WHEN** the expression cannot be evaluated
- **THEN** the response status is 400 and `ok` is false with a non-empty `error` string

### Requirement: Malformed JSON handling

If the request body is missing or not valid JSON, the endpoint SHALL treat missing fields as defaults (empty expression, `deg` mode) and SHALL still return appropriate success or error responses without server crash.

#### Scenario: Missing body

- **WHEN** the client sends POST with no JSON body
- **THEN** the server responds with 400 for empty expression rather than 500

### Requirement: Index route

The application SHALL serve the calculator page at `GET /`.

#### Scenario: Load calculator page

- **WHEN** the client requests `GET /`
- **THEN** the response is HTML containing the calculator UI
