(() => {
  const expressionEl = document.getElementById("expression");
  const resultEl = document.getElementById("result");
  const errorEl = document.getElementById("error");
  const keypad = document.getElementById("keypad");
  const equalsBtn = keypad.querySelector('[data-action="equals"]');
  const angleBtns = document.querySelectorAll(".angle-btn");

  let expression = "";
  let lastResult = "0";
  let justCalculated = false;
  let angleMode = "deg";

  const OPERATORS = new Set(["+", "-", "*", "/", "%", "^"]);

  function renderExpression() {
    expressionEl.textContent = expression || "0";
  }

  function hideError() {
    errorEl.hidden = true;
    resultEl.classList.remove("has-error");
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    resultEl.textContent = "Error";
    resultEl.classList.add("has-error");
  }

  function isOperatorChar(ch) {
    return OPERATORS.has(ch);
  }

  function startsNewNumber(ch) {
    return /\d/.test(ch) || ch === "." || ch === "(";
  }

  function insert(value) {
    hideError();

    if (justCalculated) {
      if (isOperatorChar(value)) {
        expression = lastResult;
      } else if (startsNewNumber(value) || value === "pi" || value === "e") {
        expression = "";
      } else {
        expression = lastResult;
      }
      justCalculated = false;
    }

    expression += value;
    renderExpression();
  }

  function clearAll() {
    expression = "";
    lastResult = "0";
    justCalculated = false;
    resultEl.textContent = "0";
    hideError();
    renderExpression();
  }

  function backspace() {
    if (justCalculated) {
      clearAll();
      return;
    }
    expression = expression.slice(0, -1);
    hideError();
    renderExpression();
  }

  function setLoading(loading) {
    equalsBtn.disabled = loading;
    resultEl.classList.toggle("is-loading", loading);
  }

  async function calculate() {
    const expr = expression.trim();
    if (!expr) {
      showError("Enter an expression");
      return;
    }

    hideError();
    setLoading(true);

    try {
      const res = await fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression: expr, angle_mode: angleMode }),
      });

      let data;
      try {
        data = await res.json();
      } catch {
        showError("Server returned an invalid response");
        return;
      }

      if (!data.ok) {
        showError(data.error || "Invalid expression");
        return;
      }

      const display = data.display ?? String(data.result);
      resultEl.textContent = display;
      lastResult = String(data.result);
      expression = lastResult;
      justCalculated = true;
      renderExpression();
    } catch {
      showError("Cannot connect — run: python app.py");
    } finally {
      setLoading(false);
    }
  }

  keypad.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn || btn.disabled) return;

    const action = btn.dataset.action;
    const value = btn.dataset.insert;

    if (action === "clear") {
      clearAll();
      return;
    }
    if (action === "backspace") {
      backspace();
      return;
    }
    if (action === "equals") {
      calculate();
      return;
    }
    if (value !== undefined) {
      insert(value);
    }
  });

  angleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      angleMode = btn.dataset.mode;
      angleBtns.forEach((b) => b.classList.toggle("active", b === btn));
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === "=") {
      e.preventDefault();
      calculate();
      return;
    }
    if (e.key === "Escape") {
      clearAll();
      return;
    }
    if (e.key === "Backspace") {
      e.preventDefault();
      backspace();
      return;
    }

    const map = { "*": "*", "/": "/", "+": "+", "-": "-", "%": "%", "^": "^" };
    if (map[e.key]) {
      e.preventDefault();
      insert(map[e.key]);
      return;
    }

    if (/^[0-9.()]$/.test(e.key)) {
      insert(e.key);
    }
  });

  renderExpression();
})();
