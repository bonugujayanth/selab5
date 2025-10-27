# Lab 5 — Static Code Analysis (Inventory System)

This repository contains the Lab 5 deliverables for the Static Code Analysis exercise. It includes the original `inventory_system.py`, a cleaned version `inventory_system_clean.py`, static analysis reports, and short reflection and issue documentation.

Files of interest
- `inventory_system.py` — original student file (kept for reference)
- `inventory_system_clean.py` — cleaned/fixed version that addresses several static-analysis issues
- `issues_report.md` — table summarizing issues found and fixes applied
- `reflection.md` — answers to the lab reflection questions
- `requirements.txt` — tools used for the lab (pylint, bandit, flake8)
- `.gitignore` — recommended ignores
- `pylint_report_clean.txt`, `bandit_report_clean.txt`, `flake8_report_clean.txt` — analysis outputs for the cleaned file

Quick summary of fixes
| Issue | Type | Location | Fix |
|---|---:|---|---|
| Mutable default argument | Bug | `addItem` (logs=[]) | Changed default to `None` and initialized inside function (`logs: Optional[List[str]] = None`) |
| Bare except | Bug | `removeItem`, `loadData` | Replaced with specific exception handling (FileNotFoundError, JSONDecodeError, TypeError/ValueError) and added logging |
| Use of `eval` | Security | `main()` | Removed `eval()` call and replaced with safe example/logging |
| Unsafe file I/O / JSON errors | Bug/Security | `loadData` / `saveData` | Used `with open(...)`, added JSON parsing handling and type coercion; avoided rebinding the global dict |
| Missing validation | Bug | `addItem/removeItem/getQty` | Added type checks and value checks (raise TypeError/ValueError) |
| Unprotected import-time execution | Maintainability | module top-level | Added `if __name__ == '__main__'` guard and proper logging configuration |

<!-- Reproduction instructions and notes removed as requested. -->

---

## Issues Report (full)

Below are the main issues identified and the fixes applied in `inventory_system_clean.py`.

| Issue | Type | Location | Description | Fix applied |
|---|---:|---|---|---|
| Mutable default argument | Bug | addItem logs=[] | Default list shared across calls, can cause unexpected state | Changed default to None and initialize inside function (`logs: Optional[List[str]] = None`) |
| Bare except | Bug | removeItem, loadData | Overly broad except hides errors and makes debugging hard | Catch specific exceptions (FileNotFoundError, JSONDecodeError) and handle them; use logger for unexpected errors |
| Use of eval | Security | main() | eval executes arbitrary code and is dangerous | Removed eval() usage entirely; replaced with safe logging and examples |
| Unsafe file I/O / no JSON validation | Bug/Security | loadData/saveData | Files opened without 'with' and no JSON error handling | Use with open(...), catch json.JSONDecodeError, coerce types safely |
| Missing input validation | Bug | addItem/removeItem/getQty | Functions accepted invalid types and negative quantities | Added type checks and value checks (raise TypeError/ValueError) |
| Unprotected main | Maintainability | module level | Code executed on import (no if __name__ guard) | Wrapped execution in if __name__ == '__main__' |

More minor style fixes were made to improve readability and to reduce static-analysis warnings (f-strings, logging usage, sorted iteration when printing).

---

## Reflection (full)

1. Which issues were the easiest/hardest to fix?

- Easiest: Mutable default argument and missing if __name__ guard. These are simple pattern fixes.
- Hardest: Ensuring robust JSON load/save behavior (deciding how to coerce invalid values) and choosing which exceptions to handle vs. let bubble up. These required small design decisions.

2. False positives?

- Static tools sometimes flag long function docstrings or perceived unused imports. In this exercise, most reported issues were real. A potential false positive could be a logger variable flagged as unused in some configurations, but it is used.

3. How to integrate static analysis into workflow?

- Add flake8/pylint/bandit to CI (GitHub Actions) and run them on push/PR. Configure thresholds and disable acceptable warnings per-project. Also run them locally via pre-commit hooks.

4. Improvements observed

- After fixes the code is more robust (validates inputs), more secure (no eval, handles JSON errors), and more maintainable (better logging, guarded main).

---

If you'd like these sections moved into separate files or formatted differently (for example, with line numbers or tool-specific codes), tell me how you prefer them and I will update the README.
