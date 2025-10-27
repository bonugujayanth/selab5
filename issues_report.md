# Static Analysis Issues - inventory_system.py

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
