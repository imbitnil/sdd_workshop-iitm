(() => {
  const expressionEl = document.getElementById("expression");
  const resultEl = document.getElementById("result");
  const errorEl = document.getElementById("error");
  const keypad = document.getElementById("keypad");
  const angleBtns = document.querySelectorAll(".angle-btn");

  let expression = "";
  let angleMode = "deg";

  function updateDisplay() {
    expressionEl.textContent = expression;
    hideError();
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    resultEl.classList.add("display__result--error");
  }

  function hideError() {
    errorEl.hidden = true;
    resultEl.classList.remove("display__result--error");
  }

  function insert(value) {
    expression += value;
    updateDisplay();
  }

  function clearAll() {
    expression = "";
    resultEl.textContent = "0";
    updateDisplay();
  }

  function backspace() {
    expression = expression.slice(0, -1);
    updateDisplay();
  }

  async function calculate() {
    if (!expression.trim()) return;

    hideError();
    expressionEl.textContent = expression;

    try {
      const res = await fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expression, angle_mode: angleMode }),
      });

      const data = await res.json();

      if (!data.ok) {
        showError(data.error || "Error");
        return;
      }

      resultEl.textContent = data.result;
      expression = String(data.result);
    } catch {
      showError("Could not reach server");
    }
  }

  keypad.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;

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

    const allowed = "0123456789.+-*/()%^";
    if (allowed.includes(e.key)) {
      insert(e.key);
    }
  });
})();
