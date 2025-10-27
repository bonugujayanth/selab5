# Lab 5 Reflection

1. Which issues were the easiest/hardest to fix?

- Easiest: Mutable default argument and missing if __name__ guard. These are simple pattern fixes.
- Hardest: Ensuring robust JSON load/save behavior (deciding how to coerce invalid values) and choosing which exceptions to handle vs. let bubble up. These required small design decisions.

2. False positives?

- Static tools sometimes flag long function docstrings or perceived unused imports. In this exercise, most reported issues were real. A potential false positive could be a logger variable flagged as unused in some configurations, but it is used.

3. How to integrate static analysis into workflow?

- Add flake8/pylint/bandit to CI (GitHub Actions) and run them on push/PR. Configure thresholds and disable acceptable warnings per-project. Also run them locally via pre-commit hooks.

4. Improvements observed

- After fixes the code is more robust (validates inputs), more secure (no eval, handles JSON errors), and more maintainable (better logging, guarded main).
